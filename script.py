# Requests
import requests
import csv 

#BeautifulSoup
from bs4 import BeautifulSoup

# url to scrape
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)

# Turn HTML to BeautifulSoup object
soup = BeautifulSoup(page.content, 'html.parser')

# Product Page URL
product_page_url = url
print(url)

# UPC
upc_element = soup.select_one("#content_inner > article > table > tr:nth-child(1) > td")
upc = upc_element.text
print(upc)

# Price (excl. tax)
price_excludes_tax = soup.select_one("#content_inner > article > table > tr:nth-child(3) > td")
price_excludes_tax = price_excludes_tax.text
print(price_excludes_tax)

# Price (inc. tax)
price_includes_tax = soup.select_one("#content_inner > article > table > tr:nth-child(4) > td")
price_includes_tax = price_includes_tax.text
print(price_includes_tax)

# Quantity Available
quantity_available = soup.select_one("#content_inner > article > table > tr:nth-child(6) > td")
quantity_available = quantity_available.text
print(quantity_available)

# Product Description
product_description = soup.select_one("#content_inner > article > p")
product_description = product_description.text
print(product_description)

# Category
category = soup.select_one("#default > div > div > ul > li:nth-child(3) > a")
category = category.text
print(category)

# Write scraped data to CSV
with open('book_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Header row
    writer.writerow([
        "Product Page URL", 
        "UPC", 
        "Price (excl. tax)", 
        "Price (incl. tax)", 
        "Quantity Available", 
        "Product Description", 
        "Category"
    ])
    
    # Data row
    writer.writerow([
        product_page_url, 
        upc, 
        price_excludes_tax, 
        price_includes_tax, 
        quantity_available, 
        product_description, 
        category
    ])