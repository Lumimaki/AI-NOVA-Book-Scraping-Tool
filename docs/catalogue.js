const filters = document.querySelector("#filters");
const query = document.querySelector("#query");
const rating = document.querySelector("#rating");
const sort = document.querySelector("#sort");
const results = document.querySelector("#books");
const status = document.querySelector("#results-status");
const pagination = document.querySelector("#pagination");
const previous = document.querySelector("#previous");
const next = document.querySelector("#next");
const pageNumber = document.querySelector("#page-number");
const template = document.querySelector("#book-card");
const currency = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" });
const number = new Intl.NumberFormat("en-GB");
const pageSize = 20;
const comparators = {
  title: (a, b) => a.title.localeCompare(b.title),
  "price-asc": (a, b) => a.price - b.price,
  "price-desc": (a, b) => b.price - a.price,
  rating: (a, b) => b.rating - a.rating,
};

let catalogue = [];
let page = 1;

function normalizeSearch(text) {
  return text.normalize("NFKD").replace(/\p{M}/gu, "").toLocaleLowerCase("en-GB")
    .replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}

function makeBookCard(book) {
  const card = template.content.cloneNode(true);
  const title = card.querySelector(".book-title");
  const cover = card.querySelector("img");
  cover.addEventListener("error", () => { cover.hidden = true; }, { once: true });
  cover.src = book.cover_url;
  title.href = book.product_url;
  title.textContent = book.title;
  card.querySelector(".book-author").textContent = book.author || "Author unavailable";
  card.querySelector(".price").textContent = currency.format(book.price);
  card.querySelector(".rating").textContent = `★ ${book.rating}/5`;
  card.querySelector(".availability").textContent = book.availability;
  return card;
}

function render() {
  const search = normalizeSearch(query.value);
  const terms = search ? search.split(" ") : [];
  const books = catalogue.filter(book =>
    (!rating.value || book.rating === Number(rating.value))
    && terms.every(term => book.searchText.includes(term))
  );
  if (sort.value !== "source") books.sort(comparators[sort.value]);

  const start = (page - 1) * pageSize;
  const end = Math.min(start + pageSize, books.length);
  const pageCount = Math.ceil(books.length / pageSize);
  results.replaceChildren(...books.slice(start, end).map(makeBookCard));
  status.textContent = books.length
    ? `Showing ${number.format(start + 1)}–${number.format(end)} of ${number.format(books.length)} books`
    : "No books match your filters.";
  pagination.hidden = pageCount < 2;
  previous.disabled = page <= 1;
  next.disabled = page >= pageCount;
  pageNumber.textContent = `Page ${page} of ${pageCount}`;
}

function renderFirstPage() {
  page = 1;
  render();
}

function turnPage(step) {
  page += step;
  render();
  document.querySelector("#browse-title").focus();
}

function showHeroCovers(books) {
  const hero = document.querySelector("#hero-covers");
  [books[3], books[0], books[9]].filter(Boolean).forEach(book => {
    const cover = document.createElement("img");
    cover.alt = "";
    cover.addEventListener("error", () => { cover.hidden = true; }, { once: true });
    cover.src = book.cover_url;
    hero.append(cover);
  });
}

filters.addEventListener("input", renderFirstPage);
filters.addEventListener("reset", () => requestAnimationFrame(renderFirstPage));
filters.addEventListener("submit", event => event.preventDefault());
previous.addEventListener("click", () => turnPage(-1));
next.addEventListener("click", () => turnPage(1));

async function loadCatalogue() {
  try {
    const response = await fetch("books.json");
    if (!response.ok) throw new Error(`Catalogue request failed (${response.status})`);
    const books = await response.json();
    catalogue = books.map(book => ({
      ...book,
      searchText: normalizeSearch(`${book.title} ${book.author || ""}`),
    }));
    showHeroCovers(catalogue);
    render();
    filters.hidden = false;
  } catch {
    status.textContent = "The catalogue could not load. You can still download the book table above.";
  }
}

loadCatalogue();
