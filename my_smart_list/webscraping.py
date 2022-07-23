import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import glob
import os
from ocr_core import ocr_core
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

"""Amazon URL definition"""
def get_url_amazon(search_term):
    """Generate URL with a search term"""
    template='https://www.amazon.in/s?k={}&ref=nb_sb_noss_1'
    search_term= search_term.replace(' ', '+')

    #URL query
    url= template.format(search_term)
    url+= '&page{}'

    return url

"""Amazon extract record"""
def extract_record_amazon(item):

    """Extract and return data of single record"""
    #description and URL
    atag= item.h2.a
    description= atag.text.strip()
    details_url= 'http://www.amazon.in'+ atag.get('href')
    img= item.div.div.div.div.img.get('src')

    #price
    try:
        price_parent=item.find('span','a-price')
        price= price_parent.find('span','a-offscreen').text
    except AttributeError:
        return

    #rating
    try:
        rating= item.i.text
        review_count=item.find('span',{'class':'a-size-base'}).text
    except AttributeError:
        rating=''
        review_count=''

    result= (description, price, rating, review_count, details_url,img,"Amazon")
    return result

"""Amazon web scraping driver function"""
def amazon(search_term):
    #start web driver for chrome browser
    driver = webdriver.Chrome(ChromeDriverManager().install())

    records=[]
    url= get_url_amazon(search_term)

    #First page in amazon
    for page in range(1,2):
        driver.get(url.format(page))
        soup= BeautifulSoup(driver.page_source,'html.parser')
        results= soup.find_all('div',{'data-component-type':'s-search-result'}) # find all results of items

        for item in results:
            record= extract_record_amazon(item) #passing each item from the results
            if record:
                records.append(record)

    driver.close()
    #save data to csv file
    with open('results2.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url', 'Image src','Website_Name']) #column names for the data
        writer.writerows (records)

"""Flipkart URL generate"""
def get_url(search_term):
    """Generate URL with a search term"""
    template='http://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    search_term= search_term.replace(' ', '+')

    #URL query
    url= template.format(search_term)
    return url

"""Extraction of small cards type of record"""
def extract_record_type1(item):
    #image, description and details page URL
    try:
        atag= item.div.findChildren("a")[1]
        description= atag.text.strip()
        details_url= 'http://www.flipkart.com'+ atag.get('href')
        img= item.div.a.div.div.div.img.get('src')
    except IndexError:
        return None

    #price extraction
    try:
        price= item.div.findChildren("a")[2].div.div.text.strip()
    except AttributeError:
        return "Price ERROR!"

    #ratings details extraction
    try:
        rating_spans= item.findChildren("span")
        rating= rating_spans[0].div.text.strip()
        rating_count= rating_spans[1].text.strip()
    except IndexError:
        return None
    except AttributeError:
        rating= "N/A"
        rating_count= 0
    result= (description, price, rating, rating_count, details_url,img,"Flipkart" )
    return result

"""Extraction of full screen cards type of record"""
def extract_record_type2(actual_item):
    item=actual_item.div.a
    #details
    details_url= 'http://www.flipkart.com'+item.get('href')
    #img
    img= item.div.div.div.div.img.get('src')
    #desc
    try:
     description= item.findChildren("div")[9].div.div.text.strip()
    except AttributeError:
        return None

    #price extraction
    try:
        price= item.findChildren("div")[15].div.div.div.text.strip()
    except AttributeError:
        return "Price ERROR!"

    #rating
    try:
        rating= item.findChildren("div")[12].span.div.text.strip()
        rating_count= item.findChildren("div")[12].findChildren("span")[1].span.span.text.strip()
    except IndexError:
        return None
    except AttributeError:
        rating= "N/A"
        rating_count= 0
    result= (description, price, rating, rating_count, details_url,img,"Flipkart")
    return result

"""Flipkart web scraping driver function"""
def flipkart(search_term):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    records=[]
    url= get_url(search_term)
    count=0

    for page in range(1,2):
        driver.get(url.format(page))
    #driver.get(url)
    soup= BeautifulSoup(driver.page_source,'html.parser')
    results= soup.find_all('div',{'data-id': re.compile('.*')})
    for item in results:
        try:
            if item.div.findChildren("a")[1]:
                # print(item.div.findChildren("a")[1])
                # count+=1
                record= extract_record_type1(item)
        except:
            record= extract_record_type2(item)

        # record= extract_record(item) if extract_record(item) is not None else None
        if record:
            records.append(record)
    #driver.close()
    #save data to csv file
    with open('results1.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url', 'Image src','Website_Name'])
        writer.writerows (records)

"""Consolidate the results from Amazon and Flipkart"""
def consolidate():
    # setting the path for joining multiple files (CSV files for both amazon and flipkart)
    files = os.path.join("results*.csv")

    # list of merged files returned
    files = glob.glob(files)

    print("Resultant CSV after joining all CSV files at a particular location...");

    # joining files with concat and read_csv
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df1 = df[df['Rating'].notna()]
    df1.to_csv('consolidated.csv')
    print(df1)

"""Driver function for entire web scrapping"""
def webscraping(list):
    print("webscraping", list)

    flipkart(list)
    amazon(list)
    consolidate()
