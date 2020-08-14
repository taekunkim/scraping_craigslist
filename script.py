import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
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
        images = ", ".join(images)

    except:
        images = np.NaN

    return images

def get_id(post):

    post_id = post.get('data-repost-of')

    if isinstance(post_id, int):
        return post_id

    else:
        return post.get('data-pid')

def get_last_seen():

    """
    Retrieves the date on which the listing was found the latest.
    """

    return time.asctime( time.localtime(time.time()))



names = []
prices = []
dates = []
locations = []
urls = []
imgs = []
ids = []
last_seen = []

data = {'id':        ids,
        'name':      names,
        'price':     prices,
        'date':      dates,
        'location':  locations,
        'url':       urls,
        'images':    imgs,
        'last_seen': last_seen}

def get_all_page(posts):
    for post in posts:
        names.append(get_name(post))
        prices.append(get_price(post))
        dates.append(get_date(post))
        locations.append(get_location(post))
        urls.append(get_url(post))
        imgs.append(get_img(post))
        ids.append(get_id(post))
        last_seen.append(get_last_seen())


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
        time.sleep(randint(1,5))

search_all_pages()
current = pd.DataFrame(data = data)

past = pd.read_csv('tracking.csv')
cols = ['id', 'name', 'price', 'date', 'location', 'url', 'images']

current['id']=current['id'].astype(int)
duplicate_old = past.merge(current, how = 'left', on = cols).dropna().drop('last_seen_y', axis = 1)
duplicate_old = duplicate_old.rename(columns = {'last_seen_x': 'last_seen'})

past_unique = pd.concat([past, duplicate_old, duplicate_old], sort = False).drop_duplicates(keep = False)

combined = pd.concat([past_unique, current], sort = False)
combined.to_csv('tracking.csv', index = False)