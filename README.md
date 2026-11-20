# AI Nova Book Scraping Tool

A Python scraper collects 1,000 books from [Books to Scrape](https://books.toscrape.com/).
The web catalogue lets you browse covers, search by title, filter by star rating, and sort by title, price, or rating.

- [Open the book catalogue on GitHub Pages](https://lumimaki.github.io/AI-NOVA-Book-Scraping-Tool/)
- [View all 1,000 books as a table on GitHub](docs/books.csv)
- [View the Python scraper](scraper.py)

The CSV contains each book's title, price in GBP, rating out of five, stock availability, and original product URL.
The site reads the matching [JSON export](docs/books.json), which also includes cover image URLs.
Books to Scrape is a practice catalogue, so the prices and stock labels are demo data.

## Run locally

From the repository root, start a static server:

```sh
python3 -m http.server 8000 --directory docs
```

Open [the local catalogue](http://localhost:8000/).

## Regenerate the book exports

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scraper.py
```

The scraper rewrites `docs/books.csv` and `docs/books.json`. To also upload the records to Supabase, set `SUPABASE_URL` and `SUPABASE_KEY` using [.env.example](.env.example), then run `python scraper.py --upload`.

## GitHub Pages

The site source lives in `docs/`. In the repository's **Settings → Pages**, set **Source** to **Deploy from a branch** and select **main** and **/docs**.
