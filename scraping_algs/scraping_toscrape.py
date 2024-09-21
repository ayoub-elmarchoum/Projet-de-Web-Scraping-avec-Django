#import libraries
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import time
import pandas as pd

#fetch url using requests
url="https://books.toscrape.com/"
response=requests.get(url)
#save page content
src=response.content
#print(src)
#now i have my page 
#create soup object and parse content
soup=BeautifulSoup(src,"lxml")
#print(soup)
#get all product (books)
#list where we save data
my_data=[]
#loop through pages #for all pages pagination

for page_num in range(1,3):
    url=f'https://books.toscrape.com/catalogue/page-{page_num}.html'
    response=requests.get(url)
    soup=BeautifulSoup(response.content,'lxml')
    books=soup.find_all('h3')

    for book in books:
        book_url=book.find('a')['href']
        book_response=requests.get('https://books.toscrape.com/catalogue/'+book_url)
        book_soup=BeautifulSoup(book_response.content,'lxml')
    
        #extract info (title,price,review,..)
        title=book_soup.find('h1').text
        category=book_soup.find('ul',class_="breadcrumb").find_all('a')[2].text.strip()
        rating=book_soup.find('p',class_="star-rating")['class'][1]
        price=book_soup.find('p',class_='price_color').text.strip()
        availability=book_soup.find('p',class_='availability').text.strip()
    
        my_data.append([title,category,rating,price,availability])
        print(my_data)
        print('***')
    
    
df=pd.DataFrame(my_data,columns=["title","category","Rating","price","availability"])
print(df.head(5))


#save data in csv
df.to_csv("book_data.csv",index=False)



