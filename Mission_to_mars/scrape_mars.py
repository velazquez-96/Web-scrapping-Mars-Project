from splinter import Browser
from bs4 import BeautifulSoup as bs
import pymongo
import requests
import GetOldTweets3 as got
import pandas as pd
import lxml
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #NASA Mars News
    url =  "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, "lxml")

    section = soup.find("div", class_='list_text')
    print(section)
    news_title = section.find("div", class_="content_title").text
    news_p = section.find("div", class_="article_teaser_body").text

    #PL Mars Space Images - Featured Image
    url =  "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(2)
    browser.click_link_by_partial_text("FULL IMAGE")
    browser.click_link_by_partial_text("more info")
    browser.click_link_by_partial_text(".jpg")
    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find("img")
    featured_image = image['src']
    #print(featured_image)

    #Mars Weather
    url =  "https://twitter.com/marswxreport?lang=en"
    tweetCriteria = got.manager.TweetCriteria().setUsername("MarsWxReport").setMaxTweets(1)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    user_tweet = [tweet.text for tweet in tweets]
    mars_weather = user_tweet[0]
    print(mars_weather)
    #Mars Facts

    url =  "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    facts_table = tables[0]
    facts_table.rename(columns={0:"Description", 1:"Value"}, inplace=True)
    Facts = facts_table.to_html(index=False)

    #Mars hemispheres
    url =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, "html.parser")
    items = soup.find_all('div', class_='description')

    hemisphere_image_urls = []
    for x in items:
        images_dict = {}
        title = x.a.h3.text
        browser.click_link_by_partial_text(title)
        image_url = browser.find_link_by_partial_text('Sample')['href']
        images_dict['title'] = title
        images_dict['image_url'] = image_url
        hemisphere_image_urls.append(images_dict)
        browser.back()
    print(hemisphere_image_urls)
    browser.quit()

    info_mars = {"news_title": news_title,
    "news_p":news_p,
    "featured_image":featured_image,
    "mars_weather":mars_weather,
    "Facts": Facts,
    "hemisphere_image_urls":hemisphere_image_urls}

    return info_mars



    

