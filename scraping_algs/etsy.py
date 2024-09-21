import requests
from bs4 import BeautifulSoup
import pandas as pd
# extraire des donnes et les mettre dans dictionnaire


def extract_data(div_products):
    # ici extraire chaque info (title,price,review)
    title = div_products.find(
        'h3', {'class': "wt-text-caption v2-listing-card__title wt-text-truncate"}).text.strip()
    price = "$" + div_products.find('span', {"class": "currency-value"}).text.strip()
    try:
        rating = div_products.find('span', {
                               "class": "wt-display-inline-block wt-nudge-b-1 set-review-stars-line-height-to-zero"}).text.strip()
    except AttributeError:
        try :
            rating = div_products.find(
                'span', {'class': 'wt-nudge-l-3 wt-pr-xs-1'}).text.strip()
        except:
            rating = 'no rating'
    data = {
        'title': title,
        'price': price,
        'rating': rating,
    }
    return data


def get_more_products(pageUrl):
    page = requests.get(pageUrl)
    parsed_page = BeautifulSoup(page.content, 'lxml')
    products = parsed_page.find_all('div', {"class": "v2-listing-card__info"})
    if len(products) > 0:
        product_list = [extract_data(product) for product in products]
        return product_list
    else:
        return None
