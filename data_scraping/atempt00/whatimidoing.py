from bs4 import BeautifulSoup
import requests

url = 'https://parts.cat.com/en/catcorp/shop-by-attachment#sortBy=0'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html')

print(soup)