# Requests
import requests
import csv 

#BeautifulSoup
from bs4 import BeautifulSoup

# url to scrape
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)

#See html source
print(page.content)

# Turn HTML to BeautifulSoup object
soup = BeautifulSoup(page.content, 'html.parser')