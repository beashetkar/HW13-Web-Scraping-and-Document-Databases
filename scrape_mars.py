# # MISSION TO MARS
# 
# ## Step 2 - MongoDB and Flask Application

# Dependencies

# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
from splinter import Browser
from bs4 import BeautifulSoup  
import requests
import tweepy
import yaml
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def get_file_contents(filename):
    # Return the Twitter API Keys
    try:
        with open(filename, 'r') as config_file:
            config = yaml.load(config_file)
            return (config)
    except FileNotFoundError:
        print("'%s' file not found" % filename)

# ### NASA Mars News

def get_news():
    
    # create mars data dict that we can insert into mongo
    mars_data = {}

    # Scrape the NASA Mars News Site. 
    url_news = "https://mars.nasa.gov/news/"  
    response = requests.get(url_news)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find and collect the latest Mars News 
    news_title = soup.find('div', class_="content_title").text
    news_paragraph = soup.find('div', class_="rollover_description_inner").text
    # print(news_title)
    # print(news_paragraph)

    return (news_title, news_paragraph)

# ### JPL Mars Space Images - Featured Image
# URL JPL's Featured Space Image:  https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars.

def get_featured_img():

    # Scrape the JPL Mars Space Images Site 
    url_si = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_si)
    
    # Scrape the browser into soup and find the full resolution Features image of Mars
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Collect the featured Mars Image
    image = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    return (featured_image_url)

# ### Mars Weather
# Visit the Mars Weather twitter account: https://twitter.com/marswxreport?lang=en 

def get_weather():

    TWITTER_CONFIG_FILE = 'auth.yaml'

    # Get the Twitter API Keys
    config = get_file_contents(TWITTER_CONFIG_FILE)

    # Twitter API Keys
    consumer_key = config['twitter']['consumer_key']
    consumer_secret = config['twitter']['consumer_secret']
    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']

    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target_user= "@MarsWxReport"

    # Scrape the latest Mars weather tweet from the Mars Weather twitter account
    # Search for all tweets
    mars_tweets = api.user_timeline(target_user, count=1)

    # Get the latest Mars weather tweet from home feed
    mars_weather = mars_tweets[0]["text"]
    # print(mars_weather)

    return(mars_weather)

# ### Mars Facts
# Visit the Mars Facts webpage: https://space-facts.com/mars/ 

def get_facts():

    # Scrape the Mars Facts Webpage
    url_mf = "http://space-facts.com/mars/"
    
    # With read_html function in Pandas, automatically scrape the tabular data from Mars Facts Webpage.
    mars_facts_df = pd.read_html(url_mf)[0]
    mars_facts_df.columns = ["Facts", "Data"]
    mars_facts_df.set_index("Facts", inplace=True)
    
    # With to_html method, we generate the HTML table from mars_df DataFrame.
    # mars_table_html = "".join(mars_df.to_html().split("\n"))
    mars_table_html = mars_facts_df.to_html(header=False, index=False)
    # print(mars_table_html)

    return (mars_table_html)

# ### Mars Hemispheres
# Visit the USGS Astrogeology site https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars 

def get_hemispheres():
    
    # Scrape the USGS Astrogeology site to get Mar's Hemispheres Images
    url_mh = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_mh)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #list of mars hemispheres
    hemis_mars_list = []

    # Find the number of results or images.
    results = soup.find_all('h3')

    for r in results:
        elem = r.getText()
        print(elem)
        browser.click_link_by_partial_text(elem)
    
        time.sleep(3)   # Takes time to return information
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        # Collect the full resolution image and the title of the image.
        image = soup.find("img", class_="thumb")["src"]
        img_url = "https://astrogeology.usgs.gov" + image
        #print(img_url)
        
        img_title = soup.find("h3").get_text()

        # Keep a dictionary for each hemisphere. The dictionary contains the title and the feature image.
        hemis_mars_list.append({"title": img_title, "img_url": img_url})
        browser.click_link_by_partial_text('Back')

    return (hemis_mars_list)

def scrape():

    browser = init_browser()

    (news_title, news_paragraph) = get_news()

    mars_data = { 

        "latest_news" : {
            "title"     : news_title,
            "paragraph" : news_paragraph
        },
        "featured_image" : get_featured_img(),
        "weather"       : get_weather(),
        "facts"         : get_facts(),
        "hemispheres"   : get_hemispheres()
    }

    return(mars_data)

  
    


