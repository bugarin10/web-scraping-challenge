from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from rdb_functions import clean_list
from scrapy import Selector
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url='https://redplanetscience.com'
    browser.visit(url)
    html = browser.html
    sel = Selector( text = html )

    path='//*[@class="content_title"]'
    titles=clean_list(sel.xpath(path).extract())
    title=titles[0]

    path='//*[@class="article_teaser_body"]'
    paragraphs=clean_list(sel.xpath(path).extract())
    paragraph=paragraphs[0]

    url='https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    sel = Selector( text = html )

    path='//*[@class="headerimage fade-in"]/@src'
    images_source=sel.xpath(path).extract()
    image_s=url+images_source[0]

    url='https://galaxyfacts-mars.com/'
    browser.visit(url)

    html = browser.html
    sel = Selector( text = html )

    path='//*[@class="table table-striped"]/tbody'
    table=sel.xpath(path).extract()

    table = pd.read_html(html)
    table=table[0]

    table.columns=table.iloc[0]
    table.drop(table.index[0],inplace=True)
    table.reset_index(inplace=True,drop=True)
    html_t = table.to_html()
    html_t=html_t.replace("\n","")

    url='https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    sel = Selector( text = html )

    path='//div[@class="item"]/a/@href'
    paths=sel.xpath(path).extract()

    path='//div[@class="description"]/a/h3'
    titles_img=sel.xpath(path).extract()

    titles_img=clean_list(titles_img)

    full_img_urls=[]

    for subpath in paths:
        time.sleep(3)
        url_img=url+subpath
        browser.visit(url_img)

        html = browser.html
        sel = Selector( text = html )

        path='//li/a/@href'
        sel.xpath(path).extract()
        full_img_url=sel.xpath(path).extract()[1]
        full_img_urls.append(url+full_img_url)

    browser.quit()

    hemisphere_image_urls=[]
    for i in range(4):
        hemisphere_image_urls.append({'title':titles_img[i],'img_url':full_img_urls[i]})

    scrape_mars={
        'title_news':title,
        'paragraph':paragraph,
        'image_url':image_s,
        'table':html_t,
        'images_url':hemisphere_image_urls
    }

    return scrape_mars
    