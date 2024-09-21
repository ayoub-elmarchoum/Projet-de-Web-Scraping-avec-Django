import re
import random
import string
import pandas as pd
import numpy as np
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ScrapedData
##############
# web scraping packs
from bs4 import BeautifulSoup
import requests
##############


from scraping_algs import scraping_amazon, ebay, etsy
# scraped _data view version 1
from django.core.paginator import Paginator


@login_required(login_url='login')
def scrape_v2(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        name_data = request.POST.get('data_name')
        num_page = request.POST.get('page')
        format = request.POST.get('format')
        URL = request.POST.get('url')
        user = request.user
        if name == "amazon":
            # add your user agent
            HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                        "Accept-language": 'en-US, en;q=0.5'})

            webpage = requests.get(URL, headers=HEADERS)

            soup = BeautifulSoup(webpage.content, "html.parser")

            links = soup.find_all(
                "a", attrs={"class": "a-link-normal s-no-outline"})

            links_list = []

            # Loop for extracting links from Tag Objects
            for link in links:
                links_list.append(link.get('href'))

            d = {'title': [], "price": [], "rating": [],
                 "reviews": [], "availability": []}

            # Loop for extracting product details from each link
            for link in links_list:
                new_webpage = requests.get(
                    "https://www.amazon.com" + link, headers=HEADERS)

                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                # Fun calls to display all necessary product information

                d['title'].append(scraping_amazon.get_title(new_soup))
                d['price'].append(scraping_amazon.get_price(new_soup))
                d['rating'].append(scraping_amazon.get_rating(new_soup))
                d['reviews'].append(scraping_amazon.get_review_count(new_soup))
                d['availability'].append(
                    scraping_amazon.get_availablility(new_soup))

            if format == 'csv':
                amazon_df = pd.DataFrame.from_dict(d)
                amazon_df['title'].replace('', np.nan, inplace=True)
                amazon_df = amazon_df.dropna(subset=['title'])
                amazon_df.to_csv(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.csv", header=True, index=False)
            elif format == "json":
                amazon_df = pd.DataFrame.from_dict(d)
                amazon_df['title'].replace('', pd.NA, inplace=True)
                amazon_df = amazon_df.dropna(subset=['title'])
                amazon_df.to_json(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.json", orient='records')
            else:
                amazon_df = pd.DataFrame.from_dict(d)
                amazon_df['title'].replace('', np.nan, inplace=True)
                amazon_df = amazon_df.dropna(subset=['title'])
                amazon_df.to_csv(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.csv", header=True, index=False)
                amazon_df.to_json(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.json", orient='records')
        elif name == "toscrape":
            url = "https://books.toscrape.com/"
            response = requests.get(url)
            # save page content
            src = response.content
            # print(src)
            # now i have my page
            # create soup object and parse content
            soup = BeautifulSoup(src, "lxml")
            # print(soup)
            # get all product (books)
            # list where we save data
            my_data = []
            # loop through pages #for all pages pagination

            for page_num in range(1, int(num_page)):
                url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'lxml')
                books = soup.find_all('h3')

                for book in books:
                    book_url = book.find('a')['href']
                    book_response = requests.get(
                        'https://books.toscrape.com/catalogue/'+book_url)
                    book_soup = BeautifulSoup(book_response.content, 'lxml')

                    # extract info (title,price,review,..)
                    title = book_soup.find('h1').text
                    category = book_soup.find('ul', class_="breadcrumb").find_all('a')[
                        2].text.strip()
                    rating = book_soup.find(
                        'p', class_="star-rating")['class'][1]
                    price = book_soup.find(
                        'p', class_='price_color').text.strip()
                    availability = book_soup.find(
                        'p', class_='availability').text.strip()

                    my_data.append(
                        [title, category, rating, price, availability])

            df = pd.DataFrame(my_data, columns=[
                              "title", "category", "Rating", "price", "availability"])
            if format == "csv":
                # save data in csv
                df.to_csv(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.csv", index=False)
            elif format == "json":
                df.to_json(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.json", orient='records')
            else:
                df.to_csv(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.csv", index=False)
                df.to_json(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.json", orient='records')
        elif name == "e-bay":
            data = ebay.get_more_products(URL)
            for i in range(1, int(num_page)):
                pageUrl = URL + f"&_pgn={i}"
                current_page_products = ebay.get_more_products(pageUrl)
                if current_page_products is not None:
                    data = data+current_page_products
                else:
                    break

            data_pd = pd.DataFrame.from_dict(data)
            if format == "csv":
                # save data in csv
                data_pd.to_csv(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.csv", index=False)
            elif format == "json":
                data_pd.to_json(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.json", orient='records')
            else:
                df.to_csv(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.csv", index=False)
                df.to_json(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.json", orient='records')
        elif name == "etsy":
            data = etsy.get_more_products(URL)
            # put number of pages
            for i in range(1, int(num_page)):
                pageUrl = URL + f'?ref=pagination&page={i}'
                current_page_products = etsy.get_more_products(pageUrl)
                if current_page_products is not None:
                    data = data+current_page_products
                else:
                    break
            data_pd = pd.DataFrame.from_dict(data)
            if format == "csv":
                # save data in csv
                data_pd.to_csv(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.csv", index=False)
            elif format == "json":
                data_pd.to_json(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.json", orient='records')
            else:
                df.to_csv(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.csv", index=False)
                df.to_json(
                    f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.json", orient='records')

        data = pd.read_csv(
            f"C:/Users/mouad/OneDrive/Bureau/scraped_data/{name_data}.{format}")

        paginator = Paginator(data.to_dict('records'), 20)
        page_num = request.GET.get('page')

        try:
            data = paginator.page(page_num)
        except:
            data = paginator.page(1)
        num_pages = paginator.num_pages
        num_records = len(data)

        context = {'data': data, 'paginator': paginator, 'num_pages': num_pages,
                   'num_records': num_records, 'page_num': page_num, }
        scraped_data = ScrapedData()
        scraped_data.website_url = URL
        scraped_data.user = user
        scraped_data.name_url = name

        scraped_data.save()

        messages.success(request, 'Data scraped successfully')
        messages.info(
            request, 'Please wait a few seconds to load the data into a csv file in ur desktop ')
        return render(request, 'scraped_data.html', context)

    return render(request, 'scrap.html')








def home(request):
        return render(request, "home_page.html")

# def log_sig(request):
#     return render(request, "login_sign.html")

# login view


def login_view(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username,
                            password=password, email=email)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Invalid username or password')
    context = {'page': page}
    return render(request, 'login_sign.html', context)


# generate password

def generate_pass():
    letters = string.ascii_letters
    numbers = string.digits
    password = ''.join(random.choice(letters + numbers)
                       for _ in range(10))
    return password

# register view


def regis(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password', '')
        user_photo = request.FILES.get('user_photo', None)
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        ##
        ###
        ###
        ####
        ######
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
    else:
        return render(request, 'login_sign.html')
    
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')
