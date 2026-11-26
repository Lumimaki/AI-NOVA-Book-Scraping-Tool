create table if not exists public.books (
  product_url text primary key,
  title text not null,
  price numeric(10, 2) not null check (price >= 0),
  rating integer not null check (rating between 1 and 5),
  availability text not null
);

comment on table public.books is 'Base records collected from Books to Scrape by scraper.py.';
