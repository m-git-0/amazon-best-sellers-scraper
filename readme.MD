# Scraping Amazon products

## Problem definition.
- The problem at hand is to scrape https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_ac_0_ac_1 and extract the name, Discription, rating price, link of each item in every department. This data is the to saved in a json file.

## Tools and libraries used
- Python
- playwright - for rendering javascript and avoid being blocked when i make too many requests
- Beautifulsoup - To pass the html and extract data

## code walkthrough
- The first step is to import the necessary python libraries
```python
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pprint import pprint
import time
import json
```

Then define a global variables, a dictionary that stores the output before converting it into jason and the base URL where the crawling starts
```python
department_dict = dict()

BASE_URL = 'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_ac_0_ac_1'
```

The function for extracting the requires data, `scrape()`. It takes the downloaded html and parses it using beautiful soup. This is a generator function, and it is called by the  `department()` 
### how it works


The `department()` function utilizes a number of other functions.
- `runner()` - receives a url from the `department()` function, it calls the `get_items()` functions that return a dictionary for each scraped item. This dictionary is the stored in a list. Thus is list is the return value.
- `get_items()` does it's work by calling the  `scrape()` function which does the actual data extraction. It receives the html from get_items()
- `save()` - the save function saves the scraped data into json. The save function is called whenever the user sends the `keyboard interrupt` signal. This is because it would take so long to scrape all the amazon products




