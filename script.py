# Requests
import requests
import csv 

#BeautifulSoup
from bs4 import BeautifulSoup

def scrape_book(product_page_url):
    # Request the page
    page = requests.get(product_page_url)

    # Turn HTML to BeautifulSoup object
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract fields
    upc = soup.select_one("#content_inner > article > table > tr:nth-child(1) > td").text
    price_excludes_tax = soup.select_one("#content_inner > article > table > tr:nth-child(3) > td").text
    price_includes_tax = soup.select_one("#content_inner > article > table > tr:nth-child(4) > td").text
    quantity_available = soup.select_one("#content_inner > article > table > tr:nth-child(6) > td").text
    product_description = soup.select_one("#content_inner > article > p").text
    category = soup.select_one("#default > div > div > ul > li:nth-child(3) > a").text

    # Create dictionary
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

#test that is working
category_url = "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
books_data = scrape_category(category_url)

with open('category_books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=books_data[0].keys())
    writer.writeheader()
    for book in books_data:
        writer.writerow(book)