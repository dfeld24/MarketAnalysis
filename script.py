import requests
from bs4 import BeautifulSoup  # ← This is the parser

# Define the function so can be used on any book
def getSingleBookData(url):
    
    # Step 1: Make the web request
    response = requests.get(url)

    # Step 2: Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Product Page URL
    product_page_url = url
    print(url)

    # Book Title
    book_title = soup.select_one("#content_inner > article > div.row > div.col-sm-6.product_main > h1")
    upc = book_title.text
    print(book_title)

    # UPC
    upc_element = soup.select_one("#content_inner > article > table > tr:nth-child(1) > td")
    upc = upc_element.text
    print(upc)

    # Price (excl. tax)
    price_excludes_tax = soup.select_one("#content_inner > article > table > tr:nth-child(3) > td")
    price_excludes_tax = price_excludes_tax.text
    print(price_excludes_tax)

    # Price (inc. tax)
    price_includes_tax = soup.select_one("#content_inner > article > table > tr:nth-child(3) > td")
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

# book_data = {
#     "product_page_url": url,
#     "universal_product_code": upc,
#     "book_title": book_title,
#     "price_including_tax": price_includes_tax,
#     "price_excluding_tax": price_excludes_tax,
#     "quantity_available": quantity_available,
#     "product_description": product_description,
#     "category": category
# }

# import csv

# Designate the book URL
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Call the function to get the data
book_data = getSingleBookData(url)

# Open (or create) a CSV file in write mode
# with open("book_data.csv", mode="w", newline='', encoding="utf-8") as file:
#     # Create a DictWriter and pass the field names (column headers)
#     writer = csv.DictWriter(file, fieldnames=book_data.keys())
    
#     # Write the header row
#     writer.writeheader()
    
#     # Write the book's data
#     writer.writerow(book_data)