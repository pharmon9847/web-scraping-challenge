{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# import dependencies\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as bs\n",
    "import pandas as pd\n",
    "import requests\n",
    "import time"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/usr/local/bin/chromedriver\r\n"
     ]
    }
   ],
   "source": [
    "!which chromedriver"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "def init_browser():\n",
    "    # use splinter to start Chromedriver\n",
    "    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}\n",
    "    return Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape_nasa_news():\n",
    "    news = {}\n",
    "    url = 'https://mars.nasa.gov/news'\n",
    "    response = requests.get(url)\n",
    "    soup = bs(response.text, 'html.parser')\n",
    "    #result = soup.find('li', class_='slide')\n",
    "    result = soup.find('div', class_='slide')\n",
    "    # extract the most recent news title and content\n",
    "    #news_title = result.find('li', class_=\"content_title\").find('a').text\n",
    "    news_title = result.find('div', class_=\"content_title\").find('a').text.strip()\n",
    "    news_pargrph = result.a.text.strip()\n",
    "    news[\"news_title\"] = news_title\n",
    "    news[\"news_pargrph\"] = news_pargrph\n",
    "    return news"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape_featured_image():\n",
    "    url = \"https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars\"\n",
    "    base_url = \"https://jpl.nasa.gov\"\n",
    "    \n",
    "    response = requests.get(url)\n",
    "    soup = bs(response.text, 'lxml')\n",
    "    article = soup.find(\"article\")\n",
    "    \n",
    "    featured_image_url = base_url + article.a['data-fancybox-href']\n",
    "    return featured_image_url"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape_latest_tweet():\n",
    "    url = \"https://twitter.com/marswxreport?lang=en\"\n",
    "    response = requests.get(url)\n",
    "    soup = bs(response.text, 'lxml')\n",
    "    \n",
    "    mars_weather = soup.find_all(\"p\", class_=\"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text\")[0].text\n",
    "    return mars_weather"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape_mars_facts():\n",
    "    url = 'http://space-facts.com/mars/'\n",
    "    # use pandas 'read_html' to parse the url\n",
    "    tables = pr.read_html(url)\n",
    "    df = tables[0]\n",
    "    df.columns = ['description', 'value']\n",
    "    df.set_index('description', inplace=True)\n",
    "    return df.to_html()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape_hemispheres():\n",
    "    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target$v1=Mars'\n",
    "    response = requests.get(url)\n",
    "    soup = bs(response.text, 'lxml')\n",
    "    \n",
    "    hemispheres = []\n",
    "    results = soup.find_all(\"div\", class_=\"description\")\n",
    "    \n",
    "    for results in results:\n",
    "        hemispheres.append(resulth3.text)\n",
    "        \n",
    "    #hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']\n",
    "    return hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape_hemisphere_info():\n",
    "    hemispheres = scrape_hemispheres()\n",
    "    hemisphere_info = []\n",
    "    \n",
    "    browser = init_browser()\n",
    "    \n",
    "    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "    browser.visit(url)\n",
    "    \n",
    "    for hemi in hemisphere:\n",
    "        # hemisphere\n",
    "        browser.click_link_by_partial_text(f'{hemi}')\n",
    "        \n",
    "        # create html object, parse with beautifulsoup\n",
    "        html = browser.html\n",
    "        soup = bs(html, 'html.parser')\n",
    "        # initialize dictionary\n",
    "        hemi_dict = {}\n",
    "        # scrape the incomplete url\n",
    "        inc_url = soup.find('img', class_='wide-image')['src']\n",
    "        # construct the complete url\n",
    "        img_url = 'https://astrogeology.usgs.gov' + inc_url\n",
    "        # store data in dictionary and add to tracking list\n",
    "        hemi_dict[\"title\"] = f'{hemi}'\n",
    "        hemi_dict[\"img_url\"] = img_url\n",
    "        hemisphere_info.append(hemi_dict)\n",
    "        \n",
    "        # return to original page\n",
    "        browser.click_link_by_partial_text('Back')\n",
    "        \n",
    "    browser.quit()\n",
    "    return hemisphere_info"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape():\n",
    "    mars_facts = {}\n",
    "    mars_facts[\"news_title\"] = scrape_nasa_news()[\"news_title\"]\n",
    "    mars_facts[\"news_pargrph\"] = scrape_nasa_news()[\"news_pargrph\"]\n",
    "    mars_facts[\"featured_image_url\"] = scrape_featured_image()\n",
    "    mars_facts[\"mars_weather\"] = scrape_latest_tweet()\n",
    "    mars_facts[\"mars_facts_table\"] = scrape_mars_facts()\n",
    "    mars_facts[\"hemisphere_info\"] = scrape_hemisphere_info()\n",
    "    # return dictionary\n",
    "    return mars_facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}