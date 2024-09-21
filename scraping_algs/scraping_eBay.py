from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


def get_title(soup):
    try:
        title = soup.find("h1", attrs={"class": "it-ttl"}).text.strip()
    except AttributeError:
        title = ""
    return title


def get_price(soup):
    try:
        price = soup.find("span", attrs={"itemprop": "price"}).text.strip()
    except AttributeError:
        price = ""
    return price


def get_rating(soup):
    try:
        rating = soup.find(
            "div", attrs={"class": "ebay-review-start-rating"}).text.strip()
    except AttributeError:
        rating = ""
    return rating


def get_review_count(soup):
    try:
        review_count = soup.find(
            "a", attrs={"class": "prodreview vi-VR-prodRev"}).text.strip()
    except AttributeError:
        review_count = ""
    return review_count


def get_availablility(soup):
    try:
        available = soup.find("span", attrs={"id": "qtySubTxt"}).text.strip()
    except AttributeError:
        available = "Not Available"
    return available


if __name__ == '__main__':
    URL = input('Enter a url : ')
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',"Accept-language": 'en-US, en;q=0.5'})
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    d = {'title': [], "price": [], "rating": [],"reviews": [], "availability": []}
    items = soup.find_all("div", attrs={"class": "s-item__info"})
    for item in items:
        link = item.find("a", attrs={"class": "s-item__link"})['href']
        new_webpage = requests.get(link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availablility(new_soup))
    ebay_df = pd.DataFrame.from_dict(d)
    ebay_df['title'].replace('', np.nan, inplace=True)
    ebay_df = ebay_df.dropna(subset=['title'])
    ebay_df.to_csv("ebay_data.csv", header=True, index=False)
    print(ebay_df)
