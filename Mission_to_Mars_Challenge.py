# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import Splinter and BeautifulSoup
import splinter
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# %%
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path':ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide",wait_time=1)


# %%
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# %%
slide_elem.find("div", class_='content_title')


# %%
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### Featured Images

# %%
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# %%
# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# %%
# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# %%
# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# %%
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# %%
df.to_html()


# %%
# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles


# %%
### Hemispheres


# %%
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# %%
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
img_soup = soup(html, 'html.parser')
tags = img_soup.find_all('a', class_="itemLink product-item")
for tag in tags:
    if tag.text:
        hemispheres = {}
        browser.click_link_by_partial_text("Enhanced")
        html = browser.html
        img_soup = soup(html, 'html.parser')   
        full_img_url = img_soup.find('a', text="Sample")
        img_descr = img_soup.find('h2', class_='title').get_text()
        hemispheres['img_url'] = full_img_url['href']
        hemispheres['title'] = img_descr
        hemisphere_image_urls.append(hemispheres)       


# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# %%
# 5. Quit the browser
browser.quit()


