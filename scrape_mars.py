#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time


# In[3]:


def init_browser():
    # use splinter to start Chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
init_browser()


# In[5]:


def scrape_nasa_news():
    news = {}
    url = 'https://mars.nasa.gov/news'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    #result = soup.find('li', class_='slide')
    result = soup.find('div', class_='slide')
    # extract the most recent news title and content
    #news_title = result.find('li', class_="content_title").find('a').text
    news_title = result.find('div', class_="content_title").find('a').text.strip()
    news_pargrph = result.a.text.strip()
    news["news_title"] = news_title
    news["news_pargrph"] = news_pargrph
    return news


# In[6]:


def scrape_featured_image():
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://jpl.nasa.gov"
    
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    article = soup.find("article")
    
    featured_image_url = base_url + article.a['data-fancybox-href']
    return featured_image_url


# In[7]:


def scrape_latest_tweet():
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    
    mars_weather = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text
    return mars_weather


# In[8]:


def scrape_mars_facts():
    url = 'http://space-facts.com/mars/'
    # use pandas 'read_html' to parse the url
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
    return df.to_html()


def scrape_hemispheres():
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target$v1=Mars'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    
    hemispheres = []
    results = soup.find_all("div", class_="description")
    
    for results in results:
        hemispheres.append(result.h3.text)
        
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
    return hemispheres

# In[10]:


def scrape_hemisphere_info():
    hemispheres = scrape_hemispheres()
    hemisphere_info = []
    
    browser = init_browser()
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    for hemi in hemispheres:
        # hemisphere
        browser.click_link_by_partial_text(f'{hemi}')
        
        # create html object, parse with beautifulsoup
        html = browser.html
        soup = bs(html, 'html.parser')
        # initialize dictionary
        hemi_dict = {}
        # scrape the incomplete url
        inc_url = soup.find('img', class_='wide-image')['src']
        # construct the complete url
        img_url = 'https://astrogeology.usgs.gov' + inc_url
        # store data in dictionary and add to tracking list
        hemi_dict["title"] = f'{hemi}'
        hemi_dict["img_url"] = img_url
        hemisphere_info.append(hemi_dict)
        
        # return to original page
        browser.click_link_by_partial_text
        
    browser.quit()
    return hemisphere_info


# In[11]:


def scrape():
    mars_facts = {}
    mars_facts["news_title"] = scrape_nasa_news()["news_title"]
    mars_facts["news_pargrph"] = scrape_nasa_news()["news_pargrph"]
    mars_facts["featured_image_url"] = scrape_featured_image()
    mars_facts["mars_weather"] = scrape_latest_tweet()
    mars_facts["mars_facts_table"] = scrape_mars_facts()
    mars_facts["hemisphere_info"] = scrape_hemisphere_info()
     # return dictionary
    return mars_facts


# In[ ]:




