#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager



executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the NASA mars news page
url = 'https://redplanetscience.com'
browser.visit(url)

# Add 1s delay and find class 'list_text'
browser.is_element_present_by_css('div.list_text', wait_time= 1)

news_soup = soup(browser.html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

news_title = slide_elem.find('div', class_='content_title').get_text()
news_title 

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


### Featured Images

url = 'https://spaceimages-mars.com'
browser.visit(url)

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

img_soup = soup(browser.html, 'html.parser')

img_url_rel = img_soup.find('img', class_= 'fancybox-image').get('src')

img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace= True)
df

df.to_html().split()

browser.quit()
