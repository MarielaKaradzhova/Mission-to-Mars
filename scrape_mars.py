
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path)

    # ### Visit the NASA Mars News Site

    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # %%
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')


    # %%
    slide_elem.find('div', class_='content_title')


    # %%
    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_title


    # %%
    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    news_p

    # %% [markdown]
    # ### JPL Space Images Featured Image

    # %%
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)


    # %%
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # %%
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_soup


    # %%
    # find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url_rel


    # %%
    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    img_url

    # %% [markdown]
    # ### Mars Facts

    # %%
    df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    df.head()


    # %%
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    df


    # %%
    mars_facts = df.to_html()
    mars_facts

    # %% [markdown]
    # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    # %% [markdown]
    # ### Hemispheres

    # %%
    # 1. Use browser to visit the URL 
    base_url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'

    url = base_url + "index.html"
    browser.visit(url)


    # %%
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    hemi_findall = hemisphere_soup.findAll("div",class_="description")
    hemi_findall


    # %%
    #hemi = hemi_findall[0]
    pre_hemi_urls=[]

    for hemi in hemi_findall:
        hemifind = hemi.find("a")["href"]
        hemi_url = base_url + hemifind
        pre_hemi_urls.append(hemi_url)
    pre_hemi_urls


    # %%
    #hemi_url = pre_hemi_urls[0]
    for hemi_url in pre_hemi_urls:

        browser.visit(hemi_url)
        html = browser.html
        hemisphere_soup = soup(html, 'html.parser')
        hurl = base_url + hemisphere_soup.find("div", class_="downloads").find("a")["href"]
        hemisphere_image_urls.append({
            "img_url":hurl,
            "title":"insert title here",
        })
    hemisphere_image_urls


    # %%
    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls


    # %%
    # 5. Quit the browser
    browser.quit()

    # %% [markdown]
    # # merge all scraped data into one dictionary

    # %%
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image":img_url,
        "facts": mars_facts,
        "hemispheres": hemisphere_image_urls,

    }

    return mars_data
