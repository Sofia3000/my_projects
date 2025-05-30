# started at 17.39 18.05.2025

import requests
from bs4 import BeautifulSoup
from time import sleep
import json

# url
url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page='
current = 1
# get first page
try:
    page = requests.get(f'{url}{current}').content
except:
    print(f'Can not connect to the {url}')
    exit()

# create parser
soup = BeautifulSoup(page, 'html.parser')
# get link to the last page
last_page_li = soup.find('a', {'class':'page-link', 'rel': 'next'}).find_parent('li').find_previous('li')
# get page count
try:
    page_count = int(last_page_li.text)
except:
    print('There are no information about count of pages')
    exit()

# list for laptops
laptop_info = []
while True:
    print(f'Page {current} from {page_count}')
    # get divs with laptops
    laptops = soup.find_all('div', {'class':'product-wrapper card-body'})
    # empty page
    if not laptops:
        break
    # save information about each laptop
    for laptop in laptops:
        info = {}
        # get laptop name
        info['name'] = laptop.find('a', {'class':'title'}).get('title', 'Unknown name').strip()
        # get price
        info['price'] = laptop.find('span', {'itemprop':'price'}).text
        # get description
        info['description'] = laptop.find('p', {'itemprop':'description'}).text
        # get review-count
        info['review-count'] = laptop.find('span', {'itemprop':'reviewCount'}).text
        laptop_info.append(info)
    
    # check if page is last
    if current == page_count:
        break    
    # get next page
    current += 1
    try:
        page = requests.get(f'{url}{current}').content
    except:
        print(f'Can not connect to the {url}')
        break
    # pause
    sleep(1)

# open file
fname = 'laptops.json'
with open(fname, 'w') as fhand:
    # save list to file
    json.dump(laptop_info, fhand)

print(f'All records was saved to {fname}')