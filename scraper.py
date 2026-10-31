import os
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import Client, create_client

# --- 1. LOAD CREDENTIALS FROM .env ---
# Check current directory and parent directory for .env
env_path = Path(__file__).resolve().parent / ".env"
parent_env = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
load_dotenv(dotenv_path=parent_env)

# Fallback to direct credentials if .env is missing
SUPABASE_URL = os.getenv("SUPABASE_URL") or "https://uhuzpkmsjuxffvbbfnmc.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or "sb_publishable_q0YIv_NjhYEougiYHn9Fyw___6b-512"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. CONFIGURATION ---
BASE_CATALOGUE_URL = "https://books.toscrape.com/catalogue/"
PAGE_TEMPLATE = "https://books.toscrape.com/catalogue/page-{}.html"

RATING_MAP = {
	"One": 1,
	"Two": 2,
	"Three": 3,
	"Four": 4,
	"Five": 5,
}


def extract_books_from_page(page_num):
	url = PAGE_TEMPLATE.format(page_num)
	response = requests.get(url, timeout=15)
	if response.status_code != 200:
		return []

	response.encoding = "utf-8"
	soup = BeautifulSoup(response.text, "html.parser")
	book_pods = soup.select("article.product_pod")

	page_items = []
	for pod in book_pods:
		title = pod.h3.a["title"]

		raw_price = pod.select_one(".price_color").text
		clean_price = float(re.sub(r"[^\d.]", "", raw_price))

		rating_classes = pod.select_one(".star-rating")["class"]
		rating_word = [c for c in rating_classes if c != "star-rating"][0]
		rating = RATING_MAP.get(rating_word, 0)

		availability = pod.select_one(".availability").text.strip()

		# Build clean product url
		raw_href = pod.h3.a["href"].replace("../", "").replace("catalogue/", "")
		product_url = BASE_CATALOGUE_URL + raw_href

		page_items.append(
			{
				"title": title,
				"price": clean_price,
				"rating": rating,
				"availability": availability,
				"product_url": product_url,
			}
		)

	return page_items


def scrape_all_books(total_pages=50):
	all_books = []
	print(f"Beginning crawl across {total_pages} pages...")

	for page in range(1, total_pages + 1):
		books = extract_books_from_page(page)
		all_books.extend(books)
		print(f"Scraped page {page}/{total_pages} ({len(books)} books found)")
		time.sleep(0.1)

	return all_books


def upload_to_supabase(books, batch_size=100):
	total = len(books)
	print(f"\nUploading {total} books to Supabase in batches of {batch_size}...")

	for i in range(0, total, batch_size):
		batch = books[i : i + batch_size]
		supabase.table("books").upsert(batch, on_conflict="product_url").execute()
		print(f"Uploaded {min(i + batch_size, total)}/{total} records...")


if __name__ == "__main__":
	books_data = scrape_all_books(total_pages=50)
	print(f"\nTotal books scraped: {len(books_data)}")

	upload_to_supabase(books_data, batch_size=100)
	print("\nAll 1,000 books successfully saved to Supabase!")
