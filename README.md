# Python Web Scraper — Book Catalogue

Scrapes the full book catalogue from
[books.toscrape.com](https://books.toscrape.com) (a sandbox site for scraping
practice): **title, price, star rating and availability**, following pagination
automatically. Exports to both **CSV and JSON**, and can filter by minimum
rating.

## Setup & usage
```bash
pip install -r requirements.txt

python scraper.py                          # all pages -> books.csv + books.json
python scraper.py --max 5 --min-rating 4   # first 5 pages, 4+ stars only
```

## Sample output (JSON)
```json
{
  "title": "A Light in the Attic",
  "price": "51.77",
  "rating": 3,
  "in_stock": true
}
```

## Note
Scrape responsibly — respect `robots.txt`, terms of service, and keep a
reasonable delay between requests (configurable with `--delay`).
