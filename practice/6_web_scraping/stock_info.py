"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

# https://blog.jovian.ai/web-scraping-yahoo-finance-using-python-7c4612fab70c
# https://proxiesapi-com.medium.com/scraping-most-active-stocks-data-from-yahoo-finance-with-python-and-beautiful-soup-79a218c91835

from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
# import csv 
# import pandas as pd 


def get_page(url):
    """Download a webpage and return a beautiful soup doc"""
    response = requests.get(url,  headers={'User-Agent': 'Custom'}) # python user agent was not working
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to load page {}'.format(url))
    page_content = response.text
    doc = BeautifulSoup(page_content, 'html.parser')
    return doc

url = 'https://finance.yahoo.com/most-active'
doc = get_page(url)
print('Type of doc: ', type(doc))
print(doc.find('title')) # <title>Most Active Stocks Today - Yahoo Finance</title>
div_tags = doc.find_all('div', {'class': "Ov(h) Pend(44px) Pstart(25px)"})
print(len(div_tags))