# Requests
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# ---------- STEP 1: Single-book scraper ----------
def scrape_book(product_page_url):
    # Request the page
    page = requests.get(product_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract fields
    upc = soup.select_one("#content_inner > article > table > tr:nth-child(1) > td").text
    price_excludes_tax = soup.select_one("#content_inner > article > table > tr:nth-child(3) > td").text
    price_includes_tax = soup.select_one("#content_inner > article > table > tr:nth-child(4) > td").text
    quantity_available = soup.select_one("#content_inner > article > table > tr:nth-child(6) > td").text
    product_description = soup.select_one("#content_inner > article > p").text
    category = soup.select_one("#default > div > div > ul > li:nth-child(3) > a").text

    # Data Dictionary
    book_data = {
        "Product Page URL": product_page_url,
        "UPC": upc,
        "Price (excl. tax)": price_excludes_tax,
        "Price (incl. tax)": price_includes_tax,
        "Quantity Available": quantity_available,
        "Product Description": product_description,
        "Category": category
    }
    return book_data

# ---------- STEP 2: Helper to get all book links from a single category page ----------

from urllib.parse import urljoin

def get_book_links_from_category(category_url):
    page = requests.get(category_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    book_links = []
    for a_tag in soup.select('article.product_pod h3 a'):
        relative_url = a_tag['href']
        full_url = urljoin(category_url, relative_url)
        book_links.append(full_url)

    return book_links

def scrape_category(category_url):
    all_books = []

    book_links = get_book_links_from_category(category_url)

    for link in book_links:
        book_data = scrape_book(link)
        all_books.append(book_data)

    return all_books

# ---------- STEP 3: Scrape an entire category (with pagination) ----------
def scrape_category(category_url):
    all_books = []
    current_url = category_url

    while True:
        # Get all book links on the current page
        book_links = get_book_links_from_category(current_url)

        # Scrape each book and store dictionary in the list
        for link in book_links:
            book_data = scrape_book(link)
            all_books.append(book_data)

        # Check for "next" page
        page = requests.get(current_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        next_button = soup.select_one('li.next > a')

        if next_button:
            next_url = urljoin(current_url, next_button['href'])
            current_url = next_url
        else:
            break  # No more pages

    return all_books

# ---------- STEP 4: Use it ----------
category_url = "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
books_data = scrape_category(category_url)

# Write all dictionaries to CSV
with open('category_books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=books_data[0].keys())
    writer.writeheader()
    for book in books_data:
        writer.writerow(book)

print(f"Scraped {len(books_data)} books from category.")