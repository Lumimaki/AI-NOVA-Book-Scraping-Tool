# Books Scraping Tool publication audit

This sanitized record documents the publication review performed for the AI Nova Book Scraping Tool. It does not contain credentials or private configuration values.

## Initial audit

The audit inspected the repository root, Git status, tracked files, reachable local history, scraper, dependency list, generated exports, browser interface, ignore rules, and placeholder environment example. It did not print local secret values, alter Git history, commit, push, or access a private database.

### Confirmed findings

| Finding | Action |
| --- | --- |
| The README described the catalogue and regeneration command but did not explicitly cover every course heading. | Expanded the README with purpose, collection, persistence, interaction, setup, demonstration, learning, limitations, and AI assistance. |
| The optional Supabase upload referenced credentials but provided no reproducible table definition. | Added `database/schema.sql` with the five fields uploaded by `scraper.py`, constraints, and `product_url` as the primary/upsert key. |
| No audit record was present. | Added this sanitized `AUDIT.md`. |
| A screenshot was not included. | Kept the public live catalogue as the short demonstration and added exact walkthrough steps. The course permits a screenshot or short demonstration. |
| `.env`, the nested Stillpoint repository, packaged extension files, workspace settings, and virtual environments needed to stay outside the Books repository. | Updated `.gitignore` rules exclude `.env`, `.venv/`, caches, editor and workspace settings, macOS metadata, `.pem` keys, `.crx` packages, and the separate `my-momentum/` folder. `.env.example` contains placeholders. |

### Checks that passed

- The current tracked file list contains no `.env`, private key, packaged extension, nested project, dependency folder, cache directory, or editor configuration.
- Reachable local Git object paths contain no tracked `.env` or common private-key filename; `.env.example` is intentionally tracked.
- The scraper loads Supabase credentials only from local environment variables and does not place them in the static browser files.
- The exported CSV contains 1,000 data rows with a header, and the JSON contains 1,000 records with unique product URLs.
- The public catalogue loaded and displayed 1,000 books with search, rating, sorting, pagination, source links, and a CSV download.
- The source data is attributed to Books to Scrape, and the author enrichment sources and incompleteness are documented.

## Follow-up audit

After the documentation and schema changes, the project was checked again for required README topics, placeholder configuration, accidental sensitive files, schema consistency with the upload fields, data counts, JSON/CSV validity, local static-site loading, and JavaScript syntax. The intended publication changes are limited to `README.md`, `AUDIT.md`, and `database/schema.sql`.

## Remaining limitations and unverified concerns

- The audit did not connect to or inspect the private Supabase project, so it cannot prove that a current remote table exists or contains all 1,000 records. The code and schema make the upload reproducible.
- The live interface reads the static JSON export rather than the database. The database contains only the five base scraped fields; author and cover enrichment remain in the exports.
- Author matching is incomplete and was not independently re-researched during this audit. Source URLs and match methods remain in `data/book_authors.csv`.
- The source website, cover images, bibliographic sources, and GitHub Pages are external services whose availability and terms can change.
- Automated pattern searches can miss secrets. Review the exact staged file list before publication and never add the local `.env` file.
- Existing Git history contains commit author metadata. Historical email visibility requires an explicit decision before the final push; future commits should use the configured GitHub noreply identity.
- No source-code license is included. This audit does not grant rights to external data or images.
