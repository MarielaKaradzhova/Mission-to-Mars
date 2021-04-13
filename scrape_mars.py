
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path)

    # ### Visit the NASA Mars News Site

    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    time.sleep(5)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    print(news_soup)
    slide_elem = news_soup.select_one('div.list_text')

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # ### JPL Space Images Featured Image

    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    # ### Mars Facts

    df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    mars_facts = df.to_html()

    # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

    # ### Hemispheres

    # 1. Use browser to visit the URL 
    base_url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'

    url = base_url + "index.html"
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    hemi_findall = hemisphere_soup.findAll("div",class_="description")

    #hemi = hemi_findall[0]
    pre_hemi_urls=[]

    for hemi in hemi_findall:
        hemifind = hemi.find("a")["href"]
        hemi_url = base_url + hemifind
        pre_hemi_urls.append(hemi_url)

    #hemi_url = pre_hemi_urls[0]
    for hemi_url in pre_hemi_urls:

        browser.visit(hemi_url)
        html = browser.html
        hemisphere_soup = soup(html, 'html.parser')
        hurl = base_url + hemisphere_soup.find("div", class_="downloads").find("a")["href"]
        hemisphere_image_urls.append({
            "img_url":hurl,
            "title": hemisphere_soup.find("h2", class_="title").text,
        })

    # 4. Quit the browser.
    browser.quit()

    # # merge all scraped data into one dictionary

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image":img_url,
        "facts": mars_facts,
        "hemispheres": hemisphere_image_urls,
    }
    print(mars_data)
    return mars_data

#debugging:
#scrape_all()
