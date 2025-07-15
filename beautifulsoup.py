import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def scrape_book_details(book_url):
    """
    Scrapes a single book product page from Books to Scrape and extracts details.

    Args:
        book_url (str): The URL of the book product page.

    Returns:
        dict: A dictionary containing the extracted book details, or None if scraping fails.
    """
    try:
        response = requests.get(book_url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting product_page_url
        product_page_url = book_url

        # Extracting universal_product_code (upc) - assuming it's in a table row with "UPC"
        upc_element = soup.find('th', string='UPC')
        upc = upc_element.find_next_sibling('td').text if upc_element else ''

        # Extracting book_title
        book_title = soup.find('h1').text.strip()

        # Extracting price_including_tax and price_excluding_tax
        price_including_tax_element = soup.find('th', string='Price (incl. tax)')
        price_including_tax = price_including_tax_element.find_next_sibling('td').text.strip() if price_including_tax_element else ''

        price_excluding_tax_element = soup.find('th', string='Price (excl. tax)')
        price_excluding_tax = price_excluding_tax_element.find_next_sibling('td').text.strip() if price_excluding_tax_element else ''

        # Extracting quantity_available - assuming it's in a table row with "Availability"
        quantity_available_element = soup.find('th', string='Availability')
        quantity_available = quantity_available_element.find_next_sibling('td').text.strip() if quantity_available_element else ''
        # Often the availability text is like "In stock (X available)". We need to extract the number.
        if quantity_available:
            quantity_available = ''.join(filter(str.isdigit, quantity_available))

        # Extracting product_description
        product_description_element = soup.find('div', id='product_description')
        product_description = product_description_element.find_next_sibling('p').text.strip() if product_description_element else ''

        # Extracting category
        category_element = soup.find('ul', class_='breadcrumb').find_all('a')[2]  # Assuming the category is the third item in the breadcrumb
        category = category_element.text.strip() if category_element else ''

        # Extracting review_rating - Selecting a class value
        review_rating_element = soup.find('p', class_='star-rating')
        review_rating = review_rating_element['class'][1] if review_rating_element else ''  # The second item in the class list gives the rating word (e.g., 'Two')

        # Extracting image_url - Selecting an attribute value
        image_element = soup.find('div', class_='item active').find('img')
        image_url = urljoin(book_url, image_element['src']) if image_element and 'src' in image_element.attrs else '' # Combining relative with base url

        return {
            'product_page_url': product_page_url,
            'universal_product_code': upc,
            'book_title': book_title,
            'price_including_tax': price_including_tax,
            'price_excluding_tax': price_excluding_tax,
            'quantity_available': quantity_available,
            'product_description': product_description,
            'category': category,
            'review_rating': review_rating,
            'image_url': image_url
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {book_url}: {e}")
        return None
    except Exception as e:
        print(f"Error scraping {book_url}: {e}")
        return None

def write_to_csv(data, filename='book_data.csv'):
    """
    Writes a list of dictionaries (book data) to a CSV file.

    Args:
        data (list): A list of dictionaries, where each dictionary represents a book.
        filename (str): The name of the CSV file to create.
    """
    if not data:
        print("No data to write to CSV.")
        return

    # Define the fieldnames (column headings) for the CSV
    fieldnames = [
        'product_page_url',
        'universal_product_code',
        'book_title',
        'price_including_tax',
        'price_excluding_tax',
        'quantity_available',
        'product_description',
        'category',
        'review_rating',
        'image_url'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        for row in data:
            writer.writerow(row)

    print(f"Data successfully written to {filename}")

if __name__ == "__main__":
    # Example Usage: Choose a single book URL from Books to Scrape
    book_url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    
    book_details = scrape_book_details(book_url)

    if book_details:
        write_to_csv([book_details])