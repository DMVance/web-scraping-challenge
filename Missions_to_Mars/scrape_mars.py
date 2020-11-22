from bs4 import BeautifulSoup 
import pandas as pd 
import requests, os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pymongo
import geckodriver_autoinstaller 
from webdriver_manager.firefox import GeckoDriverManager
from flask import jsonify

# profile = webdriver.FirefoxProfile()
browser = webdriver.Firefox(
            executable_path=GeckoDriverManager().install()
        )

CONN = os.getenv("CONN")
client = pymongo.MongoClient(CONN)
db = client.marscrape

def get_html(url, wait):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    driver.implicitly_wait(wait)
    html = driver.page_source
    driver.close()
    return html

def scrape():
    
    ###################################################################################################
    #### Scrape NASA Mars News ####
    
    print("""
    # ========================
    # NASA MARS NEWS SCRAPE
    # ========================
    """)

    URL = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    soup = BeautifulSoup(URL, "html.parser") # Parse HTML with Beautiful Soup

    # Retrieve the latest element that contains news title and news_paragraph
    news_t = soup.find_all("div", class_="content_title")
    for new in news_t:
        print(new)
        
    news_p = soup.find_all("div", class_="article_teaser_body")
    for newsp in news_p:
        print(newsp)
        
    news = [news_t, news_p]

    print(news_t)
    print(news_p)

    ###################################################################################################
    #### Scrape Mars Featured Image ####

    print("""
    # ========================
    # FEATURED IMAGE SCRAPE
    # ========================
    """)

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Use Selenium to scrape URL
    featured_image_html = get_html(featured_image_url, wait=5)

    # Create beautiful soup object
    soup = BeautifulSoup(featured_image_html, "html.parser")

    featured_image = soup.find_all("a", id="full_image")[0]
    # for image in images:
    image_number = featured_image["data-link"].replace("/spaceimages/details.php?id=", "")
    image_link = "https://www.jpl.nasa.gov/spaceimages/images/largesize/" + image_number + "_hires.jpg"

    featured_image_link = [image_link]

    ###################################################################################################
    #### Scrape Mars Facts ####

    print("""
    # ========================
    # MARS FACTS SCRAPE
    # ========================
    """)

    mars_facts_url = "https://space-facts.com/mars/"

    # Call selenium function to scrape url
    mars_facts_html = get_html(mars_facts_url, wait=5)

    soup = BeautifulSoup(mars_facts_html, "html.parser")

    table = soup.find_all("table")[0]
    table_html_str = str(table)

    dfs = pd.read_html(table_html_str)
    df = dfs[0]
    df = df.rename(columns={0: "Characteristic", 1: "Value"})
    # print(df)

    facts = [table_html_str]

    ###################################################################################################
    #### Scrape Mars Hemispheres ####

    print("""
    # ========================
    # MARS HEMISPHERES SCRAPE
    # ========================
    """)

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Scrape URL with Selenium
    hemispheres_html = get_html(hemispheres_url, wait=5)

    # Create BeautifulSoup object
    soup = BeautifulSoup(hemispheres_html, "html.parser")

    hemispheres = soup.find_all("a", class_="product-item")

    hemispheres_list = []

    for hemisphere in hemispheres:
        if hemisphere.find("h3"):
            hem_name = hemisphere.find("h3").text.replace("Enhanced", "").strip()
            hem_link = "https://astropedia.astrogeology.usgs.gov/download" + hemisphere["href"].replace("/search/map", "") + ".tif/full.jpg"
            hemispheres_list.append({"title": hem_name, "img_url": hem_link})

    print(hemispheres_list)

    # Mars dictionary

    print("""
    # ========================
    # FULL MARS DICTIONARY
    # ========================
    """)

    # mars_dict = {}
    mars_dict = {
        "news": news,
        "featured_image": featured_image_link,
        "facts": facts,
        "hemispheres": hemispheres_list
    }

    print(mars_dict)

    print("""
    # ------------------------
    # mongo insert...
    """)

    db.marscrape.drop()
    db.marscrape.insert_one(mars_dict)

    print("""
    # successful!
    # ------------------------
    """)

    return mars_dict


def get_mongo_dict():

    print("""
    # ========================
    # MONGO QUERY
    # ========================
    """)

    mongo_dict = db.marscrape.find_one()

    print(type(mongo_dict))
    # for key, value in mongo_dict.items():
    #     print(key)
    #     print(value)
    
    return mongo_dict
