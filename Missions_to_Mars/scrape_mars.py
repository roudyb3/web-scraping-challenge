#import dependencies
import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #add in Mars page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html

    #create the beautiful soup object
    soup = bs(html, 'html.parser')
    #print(soup.title.text)
    #print(soup.prettify())

    #find the titles
    title = soup.find_all('div', class_='content_title')
    news_title = title[0].text
    #print(news_title)

    paragraph = soup.find_all('div', class_ = 'article_teaser_body')
    news_p = paragraph[0].text
    #print(news_p)

    #Step 2 -- getting the images from the mars space image site

    url_img = 'https://spaceimages-mars.com/'
    browser.visit(url_img)

    #create the beautiful soup object
    html_img = browser.html
    soup_img = bs(html_img, 'html.parser')
    # print(soup_img.title.text)


    browser.links.find_by_partial_text('FULL IMAGE').click()
    img = soup_img.find_all('a', class_= 'showimg fancybox-thumbs')

    for i in img:
        featured_image_url = (url_img + i['href'])
        
    # print(featured_image_url)

    url = 'https://galaxyfacts-mars.com/'

    #step 3 -- mars facts, bring in the tables from the galaxy facts website
    tables = pd.read_html(url)
    # print(tables)

    #check the total number of tables pandas found
    # print(len(tables))

    #check out which table we need of the 2
    # print(tables[0])

    #turn the table into a dataframe
    mars_df = tables[0]

    #Change the column names
    mars_df = mars_df.rename(columns={0: 'Parameters', 1: "Mars", 2: "Earth"})

    mars_df = mars_df.drop(0)

    #Set the index
    mars_df = mars_df.set_index('Parameters')

    html_table = mars_df.to_html()

    mars_df.to_html('mars_df.html')

    # !open mars_df.html

    #Step 4 -- add in Mars Hemisphere page to scrape images
    url_hem = 'https://marshemispheres.com/'
    browser.visit(url_hem)

    #create the beautiful soup object
    html = browser.html
    soup = bs(html, 'html.parser')
    soup.title.text

    img_list = soup.find_all('a', class_= 'itemLink product-item')

    hrefs = []
    for x in img_list:
        hrefs.append(x['href'])
    hrefs = hrefs[:-1]
    hrefs = list(set(hrefs))

    final_image_urls = []
    for href in hrefs:

        img_url = url_hem + href
        browser.visit(img_url)

        html = browser.html
        soup = bs(html, 'html.parser')

        urls = soup.find_all('a', text='Sample')

        final_image_url = url_hem + urls[0]['href']
        final_image_urls.append(final_image_url)
        
    #print(final_image_urls)

    mongo_dictionary = {'news_title': news_title, 
                    'news_p': news_p, 
                    'featured_image_url': featured_image_url, 
                    'html_table': html_table, 
                    'final_image_urls': final_image_urls}
    print(mongo_dictionary)

    browser.quit()
    
    return mongo_dictionary