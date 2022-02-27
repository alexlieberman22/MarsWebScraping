#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime as dt
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_para = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_para,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres" : hemisphere_data(browser)
    }

    browser.quit()
    return data


### Visit the NASA mars news page
def mars_news(browser):
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Add 1s delay and find class 'list_text'
    browser.is_element_present_by_css('div.list_text', wait_time= 1)

    news_soup = soup(browser.html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')

        news_title = slide_elem.find('div', class_='content_title').get_text()

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title , news_p


### Featured Images
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    img_soup = soup(browser.html, 'html.parser')

    try:
        img_url_rel = img_soup.find('img', class_= 'fancybox-image').get('src')
    
    except AttributeError:
        return None

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


### Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace= True)

    return df.to_html()

### Hemispheres
def hemisphere_data(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    hem_soup = soup(browser.html, 'html.parser')
    hem_soup = hem_soup.find('div', class_='collapsible results')
    hem_soup = hem_soup.find_all('div', class_='item')

    for item in hem_soup:
        title = item.find('h3').get_text()
        browser.links.find_by_partial_text(item.find('h3').get_text()).click()
        
        img_soup = soup(browser.html, 'html.parser')
        img_soup = img_soup.find('div', class_='downloads')
        img = img_soup.find('a').get('href')

        hemisphere_image_urls.append({'img_url':img, 'title': title})

        browser.back()

    # 4. Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


#If running as script, just print the scraped data
if __name__ == '__main__':
    print(scrape_all())