#import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

#create path to directory where chrome driver exists
def init_browser():
   executable_path = {'executable_path': 'chromedriver'}
   return Browser('chrome', **executable_path, headless=False)

# Scraping Nasa Mars News Site
def scrape():
   browser = init_browser()
   data = {}

   #url to the page
   url = 'https://mars.nasa.gov/news/'

   #visit the url
   browser.visit(url)

   #use beautiful soup to html
   html = browser.html
   news_soup = BeautifulSoup(html, 'html.parser')

   #print latest news aritcle and parapgraph
   first_title = news_soup.find('div', class_="content_title")

   paragraph = news_soup.find('div', class_="article_teaser_body")

   #appending to dictionary
   data['first_title'] = first_title.text
   data['paragraph'] = paragraph.text

# Scraping JPL Mars Space Featured Image

   #url to page
   url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

   #visit url
   browser.visit(url)

   time.sleep(1)

   #click full image
   browser.click_link_by_partial_text('FULL IMAGE')

   # browser.click_link_by_partial_text('more info')
   time.sleep(1)

   #use beautiful soup to html
   html = browser.html
   image_soup = BeautifulSoup(html, 'html.parser')

   #scrape the url
   url = "https://www.jpl.nasa.gov"

   #scrape the url
   image_path = image_soup.find('img', class_="fancybox-image")["src"]

   url = "https://www.jpl.nasa.gov"

   featured_image_url = url + image_path

   data['featured_image_url'] = featured_image_url

# Scrape Mars Weather (latests Mars weather Tweet)

   #url to page
   url = "https://twitter.com/marswxreport?lang=en"

   #visit the page
   browser.visit(url)

   #use beautiful soup to html
   html = browser.html
   weather_soup = BeautifulSoup(html, 'html.parser')

   mars_weather = weather_soup.find('p', class_="TweetTextSize").text

   data['mars_weather'] = mars_weather

# Use Pandas to scrape table containing facts about Mars
   #url to page
   url = "https://space-facts.com/mars/"

   #pull the table from the website
   tables = pd.read_html(url)

   #select the first table on the website and convert to dataframe
   df = tables[0]

   #change table column names
   df.columns = ['Description:', 'Value:']

   #set index to description
   df.set_index('Description:', inplace=True)

   #convert the data to a HTML table string
   html_table = df.to_html()

   data['facts'] = html_table
# Obtain high resolution images for each of Mar's hemispheres

   #url to page
   url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

   #visit the page
   browser.visit(url)

   #use beautiful soup to html
   html = browser.html
   hemi_soup = BeautifulSoup(html, 'html.parser')

   #create an empty list
   hemisphere_image_urls = []

   #find all 4 hemisphere information
   results = hemi_soup.find_all('div', class_ = 'item')

   #base url
   base_url = 'https://astrogeology.usgs.gov'

#loop through each result to extract the title and url to each image
   for result in results:
       title = result.find('h3').text

       hemisphere_url = result.find('a', class_='itemLink')

       link = hemisphere_url['href']

       image_link = base_url + link

       browser.visit(image_link)

       html = browser.html

       each_hemi_soup = BeautifulSoup(html, 'html.parser')

       image = each_hemi_soup.find('img', class_='wide-image')['src']

       image_url = base_url + image

       hemisphere_image_urls.append({'Title':title, "URL" :image_url})

   data['hemispheres'] = hemisphere_image_urls

   #close browser window after scraping is done
   browser.quit()

   return data