#import the necessary libraries
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pprint import pprint
import time
import json
#from bestseller2 import runner
department_dict = dict()

BASE_URL = 'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_ac_0_ac_1'

def scrape(html=None):
    soup = BeautifulSoup(html,'html.parser')
    tags = soup.find_all('div',id='gridItemRoot')

    for tag in tags:
        if tag.name:
            desc = tag.find('div','_cDEzb_p13n-sc-css-line-clamp-3_g3dy1')
            rating = tag.find('span','a-icon-alt')
            price = tag.find('span','a-size-base a-color-price')
            link = tag.find('a',role='link')

            if desc and rating and price and link:
                price_range = ''.join(price.get_text().strip().split())
                name = desc.get_text().strip().split(',')[0]
                yield{
                    name:{
                        'Description':desc.get_text().strip(),
                        'rating':" ".join(rating.get_text().strip().split()),
                        'price':price_range,
                        'link':'https://www.amazon.com'+link.get('href')
                    }
                }


def department(url):

    def get_items(start_url):
        page.goto(start_url)
        #wait for the page to load
        page.wait_for_timeout(1000)
        
        #extract the part of the page we are interested in
        html = page.inner_html('div#zg-right-col')

        while html:
            #TODO: scrape html
            for x in scrape(html):
                yield x
            soup = BeautifulSoup(html,'html.parser')

            n = soup.find('li','a-last')
            if n:
                try:
                    link = n.a.get('href')
                    new_page = 'https://www.amazon.com'+link
                    page.goto(new_page)
                    page.wait_for_timeout(1000)

                    html = page.inner_html('div#zg-right-col')
                    continue
                except Exception as e:
                    break
            else:
                break
#=================================================================================
    def runner(url):
        #pass in a link and get a list of scraped items as dictionaries
        scraped = []
        for item in get_items(url):
            scraped.append(item)

        return scraped

#===================================================================================
    category_dict = dict()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=50)
        page = browser.new_page()
        page.goto(url)

        #get the html
        html = page.inner_html('div._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz')
        soup = BeautifulSoup(html,'html.parser')
        link_tags = soup.find_all('div',role='treeitem')

        
        #iterate through the departments
        for item in link_tags:
            if item.name:
                name = item.get_text().strip()
                link = 'https://www.amazon.com'+item.a.get('href')
                print('scraping....',name)

                page.goto(link)
                first_cat_html = page.inner_html('div._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz')
                first_cat_soup = BeautifulSoup(first_cat_html,'html.parser')
                first_cat = first_cat_soup.find('div','_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz',role="group").children
                if first_cat:
                    #the list is not empty so i need to extract the links and follow them
                    for group_item in first_cat:
                        if group_item.name:
                            name2 =  group_item.get_text().strip()
                            link2 = 'https://www.amazon.com'+group_item.a.get('href')
                            scraped_items = runner(link2)
                            
                            print('\tscraping...',name2)
                            category_dict[name2] = scraped_items
                            
                    department_dict[name] = category_dict
        save(department_dict)


def save(d):
    with open('final.json','w')as f:
        json.dump(d,f,indent=4)                       

if __name__ == '__main__':
    try:
        department(BASE_URL)
    except KeyboardInterrupt:
        print('Interrupted')
        save(department_dict)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
