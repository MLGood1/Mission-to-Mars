# Import Splinter, BeautifulSoup, and Pandas

from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Define scrape_all function
def scrape_all():

    # Set up splinter executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "mars_hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data

# Create mars_news function
def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')
    
        # Use the parent element to find the first string 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

# Define function
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup

    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
   
    except AttributeError:
        return None
     

    # Use the base URL to create an absolute URL

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# Define function
def mars_facts():

    # Add try/except for error handling
    try:

        # Scrape entire Mars Facts table using Pandas .read_html()
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe 
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert DataFrame to HTML
    return df.to_html()


# Create mars_hemispheres function
def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 

    url = 'https://marshemispheres.com/'
    browser.visit(url + 'index.html')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    
    # Iterate through the html

    for i in range(4):

        # Find and click each hemisphere link   
        hemi_image_elem = browser.find_by_tag('h3')[i]
        hemi_image_elem.click()
 
        # Parse HTML with beautiful soup

        html = browser.html
        hemi_img_soup = soup(html, 'html.parser')
    
        # scrape html for image
    
        hemi_image_url_rel = hemi_img_soup.find('li').a['href']

        # Use the base URL to create an absolute URL

        hemi_img_url = f'https://marshemispheres.com/{hemi_image_url_rel}'
    
        #scrape html for title
    
        title = hemi_img_soup.find('h2', class_='title').text
        
        # Store findings in a dictionary and append list
    
        hemispheres = {
        'image_url': hemi_img_url, 
        'title': title,
        }
        hemisphere_image_urls.append(hemispheres)
    
        # Use browser.back() to navigate back to the beginning to get the next hemisphere image.
    
        browser.back()
      
    return hemisphere_image_urls

if __name__=="__main__":
    # If running as script, print scraped data
    print(scrape_all())







