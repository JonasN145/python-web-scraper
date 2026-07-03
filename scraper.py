#!/usr/bin/env python3
"""Scrape the book catalogue from books.toscrape.com to CSV and JSON.

books.toscrape.com is a sandbox site built specifically for scraping practice.
This collects every book's title, price, star rating and stock availability,
follows pagination automatically, and can filter by minimum rating.

Usage:
    python scraper.py                          # all pages -> books.csv + books.json
    python scraper.py --max 5 --min-rating 4   # first 5 pages, 4+ stars only
"""
import argparse
import csv
import json
import time

import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/catalogue/"
START = "https://books.toscrape.com/catalogue/page-1.html"
RATING = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_page(url):
    resp = requests.get(url, timeout=10, headers={"User-Agent": "book-scraper/1.0"})
    resp.raise_for_status()
    resp.encoding = "utf-8"   # site is UTF-8; avoids the £ turning into "Â£"
    soup = BeautifulSoup(resp.text, "html.parser")

    books = []
    for pod in soup.select("article.product_pod"):
        rating_class = pod.select_one("p.star-rating")["class"][1]  # e.g. "Three"
        books.append({
            "title": pod.h3.a["title"],
            "price": pod.select_one("p.price_color").get_text(strip=True).lstrip("£"),
            "rating": RATING.get(rating_class, 0),
            "in_stock": "In stock" in pod.select_one("p.instock.availability").get_text(),
        })

    nxt = soup.select_one("li.next > a")
    next_url = BASE + nxt["href"] if nxt else None
    return books, next_url


def main():
    parser = argparse.ArgumentParser(description="Scrape books.toscrape.com.")
    parser.add_argument("--max", type=int, default=0, help="Max pages (0 = all)")
    parser.add_argument("--min-rating", type=int, default=0, help="Keep books with >= this rating")
    parser.add_argument("--csv", default="books.csv")
    parser.add_argument("--json", default="books.json")
    parser.add_argument("--delay", type=float, default=0.3)
    args = parser.parse_args()

    all_books, url, page = [], START, 0
    while url:
        page += 1
        print(f"Scraping page {page} …")
        books, url = parse_page(url)
        all_books.extend(books)
        if args.max and page >= args.max:
            break
        time.sleep(args.delay)

    if args.min_rating:
        all_books = [b for b in all_books if b["rating"] >= args.min_rating]

    with open(args.csv, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["title", "price", "rating", "in_stock"])
        writer.writeheader()
        writer.writerows(all_books)
    with open(args.json, "w", encoding="utf-8") as fh:
        json.dump(all_books, fh, indent=2, ensure_ascii=False)

    print(f"\nDone — {len(all_books)} books saved to {args.csv} and {args.json}")


if __name__ == "__main__":
    main()
