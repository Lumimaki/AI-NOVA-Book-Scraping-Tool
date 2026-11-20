import argparse
import csv
import json
import os
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

CATALOGUE_URL = "https://books.toscrape.com/catalogue/"
OUTPUT_DIR = Path(__file__).resolve().parent / "docs"
RATINGS = {name: value for value, name in enumerate(("One", "Two", "Three", "Four", "Five"), 1)}
TABLE_FIELDS = ("title", "price", "rating", "availability", "product_url")


def extract_books_from_page(page_num):
    page_url = urljoin(CATALOGUE_URL, f"page-{page_num}.html")
    response = requests.get(page_url, timeout=15)
    response.raise_for_status()
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    books = []
    for pod in soup.select("article.product_pod"):
        title_link = pod.select_one("h3 a")
        rating = next(RATINGS[name] for name in pod.select_one(".star-rating")["class"] if name in RATINGS)
        books.append({
            "title": title_link["title"],
            "price": float(pod.select_one(".price_color").get_text(strip=True).removeprefix("£")),
            "rating": rating,
            "availability": pod.select_one(".availability").get_text(strip=True),
            "product_url": urljoin(page_url, title_link["href"]),
            "cover_url": urljoin(page_url, pod.select_one("img")["src"]),
        })
    if not books:
        raise ValueError(f"No books found on {page_url}")
    return books


def scrape_all_books(total_pages=50):
    books = []
    for page_num in range(1, total_pages + 1):
        page = extract_books_from_page(page_num)
        books.extend(page)
        print(f"Scraped page {page_num}/{total_pages} ({len(page)} books)")
        time.sleep(0.1)
    if len({book["product_url"] for book in books}) != len(books):
        raise ValueError("Duplicate book URLs found in the catalogue")
    return books


def export_books(books):
    OUTPUT_DIR.mkdir(exist_ok=True)
    with (OUTPUT_DIR / "books.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=TABLE_FIELDS, lineterminator="\n")
        writer.writeheader()
        for book in books:
            row = {field: book[field] for field in TABLE_FIELDS}
            row["price"] = f'{row["price"]:.2f}'
            writer.writerow(row)
    with (OUTPUT_DIR / "books.json").open("w", encoding="utf-8") as output:
        json.dump(books, output, ensure_ascii=False, indent=2)
        output.write("\n")


def upload_to_supabase(books, batch_size=100):
    from dotenv import load_dotenv
    from supabase import create_client

    load_dotenv(Path(__file__).resolve().parent / ".env")
    client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    for start in range(0, len(books), batch_size):
        batch = [{field: book[field] for field in TABLE_FIELDS} for book in books[start:start + batch_size]]
        client.table("books").upsert(batch, on_conflict="product_url").execute()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Books to Scrape and export the GitHub catalogue.")
    parser.add_argument("--upload", action="store_true", help="Also upsert the books into Supabase using .env.")
    args = parser.parse_args()
    books = scrape_all_books()
    export_books(books)
    print(f"Exported {len(books)} books to docs/books.csv and docs/books.json.")
    if args.upload:
        upload_to_supabase(books)
        print(f"Upserted {len(books)} books into Supabase.")
