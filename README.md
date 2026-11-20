# AI Nova Book Scraping Tool

A Python scraper collects 1,000 books from [Books to Scrape](https://books.toscrape.com/).
The web catalogue lets you browse covers, search by title or author, filter by star rating, and sort by title, price, or rating.

- [Open the book catalogue on GitHub Pages](https://lumimaki.github.io/AI-NOVA-Book-Scraping-Tool/)
- [View all 1,000 books as a table on GitHub](docs/books.csv)
- [View the Python scraper](scraper.py)

The CSV contains each book's title, author when available, price in GBP, rating out of five, stock availability, and original product URL.
The site reads the matching [JSON export](docs/books.json), which also includes cover image URLs.
Books to Scrape is a practice catalogue, so the prices and stock labels are demo data.

## Run locally

From the repository root, start a static server and leave it running:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory docs
```

Open [the local catalogue](http://127.0.0.1:8000/).

## Development workflow

1. **Initial catalogue.** Scraped 50 listing pages, exported 1,000 books, and published a title-searchable catalogue and CSV on GitHub.
2. **Author search.** Matched catalogue records against bibliographic sources, added an author column to both exports, and updated the search and book cards. Try **Sarah Waters** for *Tipping the Velvet*, **Silverstein** for *A Light in the Attic*, or **Marie Kondo** for books credited to Marie Kondō.

See the [commit history](https://github.com/Lumimaki/AI-NOVA-Book-Scraping-Tool/commits/main/) and [GitHub Pages workflow runs](https://github.com/Lumimaki/AI-NOVA-Book-Scraping-Tool/actions) for the published changes.

### Author data

Author credits are available for **723 of 1,000 books**. Books to Scrape does not provide a dedicated author field. The [author matches file](data/book_authors.csv) records the source and match method for each credit. Matches use distinctive titles, agreement with [catalogue descriptions](https://github.com/Lucas382/ScrapyTemplate/blob/master/bookdata.csv), or a direct bibliographic reference. Titles with uncertain matches still appear in title searches and show **Author unavailable**.

The main references were [Best Books Ever by Lorena Casanova Lozano and Sergio Costa Planells (CC BY-NC 4.0)](https://doi.org/10.5281/zenodo.4265096), [Goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k), and [Open Library](https://openlibrary.org/).

## Regenerate the book exports

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scraper.py
```

The scraper joins the checked-in [author matches](data/book_authors.csv) by product URL before writing `docs/books.csv` and `docs/books.json`. To also upload the base scraped fields to Supabase, set `SUPABASE_URL` and `SUPABASE_KEY` using [.env.example](.env.example), then run `python scraper.py --upload`.

## GitHub Pages

The site source lives in `docs/`. In the repository's **Settings → Pages**, set **Source** to **Deploy from a branch** and select **main** and **/docs**.
