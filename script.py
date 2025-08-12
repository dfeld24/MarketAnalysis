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

#test that is working
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
book_info = scrape_book(url)
print(book_info)

with open('book_data.csv', mode='w', newline='', encoding='utf-8') as file:
    # Create a DictWriter using the dictionary keys as column names
    writer = csv.DictWriter(file, fieldnames=book_info.keys())
    
    # Write the header row
    writer.writeheader()
    
    # Write the single row of book data
    writer.writerow(book_info)