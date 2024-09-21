import requests
from bs4 import BeautifulSoup
import pandas as pd
#extraire des donnes et les mettre dans dictionnaire
def extract_data(div_product):
    #ici extraire chaque info (title,price,review)
    title=div_product.find('div',{'class':'s-item__title'}).find('span').text.strip()
    price=div_product.find('span',{'class':"s-item__price"}).text.strip()
    data={
        'title':title,
        'price':price,
        
    }
    return data

def get_more_products(pageUrl):
    page=requests.get(pageUrl)
    parsed_page=BeautifulSoup(page.content,'lxml')
    products=parsed_page.find_all('div',{'class':'s-item__info clearfix'})
    if len(products)>0:
        product_list=[extract_data(product) for product in products ]
        return product_list
    else:
        return None