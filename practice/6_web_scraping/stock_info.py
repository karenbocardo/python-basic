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
# from lxml import etree
# import csv 
import pandas as pd
from tabulate import tabulate


def get_page(url):
    """Download a webpage and return a beautiful soup doc"""
    response = requests.get(url,  headers={'User-Agent': 'Custom'}) # python user agent was not working
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to load page {}'.format(url))
    page_content = response.text
    doc = BeautifulSoup(page_content, 'html.parser')
    return doc

def get_results_number(soup):
    results = soup.find('span', attrs={'class':'Mstart(15px) Fw(500) Fz(s)'}) # 1-47 of 47 results
    return int(results.text.split()[2])

def get_table_header(soup):
    """Return Table columns in list form """
    header = soup.findAll('th')
    header_list = [item.text for index, item in enumerate(header)]
    return header_list

def get_table_rows(soup):
    data = []
    table = soup.find('table', attrs={'class':'W(100%)'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # get rid of empty values
    
    return data

'''
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
    statistics tab: https://finance.yahoo.com/quote/TSLA/key-statistics?p=TSLA
'''
'''
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.
    holders tab: https://finance.yahoo.com/quote/TSLA/holders?p=TSLA
'''

def get_stock_ceo(symbol):
    url = f'https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}'
    soup = get_page(url)
    # header: ['Name', 'Title', 'Pay', 'Exercised', 'Year Born']
    rows = get_table_rows(soup)
    ceo = rows[0] # first row is ceo
    return ceo


'''
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
    profile tab: https://finance.yahoo.com/quote/TSLA/profile?p=TSLA
'''
def read_profile(data, symbol):
    ceo = get_stock_ceo(symbol)
    name = ceo[0]
    year = ceo[4]
    data.loc[symbol, 'CEO Name'] = name
    data.loc[symbol, 'CEO Year Born'] = year
    
def read_all_stocks(data, rows):
    ceos = list()
    count = 1
    for symbol, row in data.head().iterrows(): # only first five for the moment
        #print(symbol, row['Name'])
        name = row['Name']
        print(f'[{count}] reading {name}')
        read_profile(data, symbol)
        count += 1
    print(data.head())

def scrape_yahoo_most_active(url):
    data = pd.DataFrame()
    soup = get_page(url)

    res_num = get_results_number(soup)
    print(f'reading {res_num} results')

    header = get_table_header(soup) # ['Symbol', 'Name', 'Price (Intraday)', 'Change', '% Change', 'Volume', 'Avg Vol (3 month)', 'Market Cap', 'PE Ratio (TTM)', '52 Week Range']
    rows = get_table_rows(soup) 

    data = pd.DataFrame([row[:2] for row in rows], columns=header[:2])
    data = data.set_index('Symbol')
    print(data.head())

    read_all_stocks(data, rows)

BASE_URL = 'https://finance.yahoo.com'
# url = 'https://finance.yahoo.com/most-active'
url = 'https://finance.yahoo.com/most-active?offset=0&count=100' # hundred most active
scrape_yahoo_most_active(url)