import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from datetime import datetime
from time import sleep
import numpy as np
from random import randint

HEADERS = ({'User-Agent':      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def get_name(post):
    try:
        name = post.find('a', class_ = 'result-title hdrlnk').text

    except:
        name = np.NaN

    return name

def get_price(post):
    try:
        price = int(post.a.text[1:])

    except:
        pass

    try:
        price = int(post.find('span', class_ = 'result-price').text[1:])

    except:
        price = np.NaN

    return price

def get_date(post):
    date = post.find('time')

    return date['datetime']

def get_location(post):
    try:
        location = post.find('span', class_ = 'result-hood').text[2:-1]

    except:
        location = np.NaN

    return location

def get_url(post):
    url = post.a['href']
    return url

def get_img(post):
    try:
        anchor_tag = post.find('a', class_ = 'result-image gallery')
        image_ids = anchor_tag.get('data-ids').split(',')
        product_ids = [image_id[2:] for image_id in image_ids]

        images = [IMG_URL.format(product_id) for product_id in product_ids]

    except:
        images = np.NaN

    return images

def get_id(post):

    post_id = post.get('data-repost-of')

    if isinstance(post_id, int):
        return post_id

    else:
        return post.get('data-pid')

names = []
prices = []
dates = []
locations = []
urls = []
imgs = []
ids = []

data = {'id':       ids,
        'name':     names,
        'price':    prices,
        'date':     dates,
        'location': locations,
        'url':      urls,
        'images':   imgs}

def get_all_page(posts):
    for post in posts:
        names.append(get_name(post))
        prices.append(get_price(post))
        dates.append(get_date(post))
        locations.append(get_location(post))
        urls.append(get_url(post))
        imgs.append(get_img(post))
        ids.append(get_id(post))


URL = 'https://sandiego.craigslist.org/search/sss?query=desk+chair&sort=rel&s='
IMG_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def search_all_pages():
    n = 0

    while True:
        url = URL + str(n)
        response = requests.get(url, headers = HEADERS)

        if response.status_code != 200:
            return 'Cannot access website'

        html_soup = BeautifulSoup(response.text, features="lxml")
        results = html_soup.find_all('li', class_ = 'result-row')
        get_all_page(results)

        n += 120
        total_count = html_soup.find('span', class_ = 'totalcount').text
        if n > int(total_count):
            break
        sleep(randint(1,5))

search_all_pages()
latest = pd.DataFrame(data = data)

past = pd.read_csv('tracking.csv')
combined = pd.concat([past, latest], sort = False)
combined = combined.groupby(['id', 'date']).first()
combined.to_csv('tracking.csv')


# In[ ]:
