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
from lxml import etree
# import csv 
import pandas as pd
from tabulate import tabulate
from lxml import html
import os
from datetime import datetime
import re

def file_with_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname( __file__ ), filename))

def get_response(url):
    """Download a webpage and return a beautiful soup doc"""
    response = requests.get(url,  headers={'User-Agent': 'Custom'}) # python user agent was not working
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to load page {}'.format(url))
    return response

def get_page(url):
    response = get_response(url)
    page_content = response.text
    doc = BeautifulSoup(page_content, 'html.parser')
    return doc

def get_results_number(soup):
    results = soup.find('span', attrs={'class':'Mstart(15px) Fw(500) Fz(s)'}) # 1-47 of 47 results
    return int(results.text.split()[2])

def get_table_header(soup, table_number=0):
    """Return Table columns in list form """
    table = soup.findAll('table')[table_number]
    header = table.findAll('th')
    header_list = [item.text for item in header]
    return header_list

def get_table_rows(soup, table_number=0, table_class="W(100%)"):
    data = []
    #table = soup.table
    #table = soup.find("table",attrs={"class":table_class})
    # table_body = table.tbody 
    table = soup.findAll('table')[table_number]
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # get rid of empty values
    
    return data

'''
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
    profile tab: https://finance.yahoo.com/quote/TSLA/profile?p=TSLA
'''
def stock_tab_url(tab, symbol):
    return f'{BASE_URL}/quote/{symbol}/{tab}?p={symbol}'

def read_profile(data, symbol):
    # @TODO change to search row with 'CEO' in title,
    # right now it is reading first row
    url = stock_tab_url('profile', symbol)
    soup = get_page(url)
    # header: ['Name', 'Title', 'Pay', 'Exercised', 'Year Born']
    rows = get_table_rows(soup)
    ceo = rows[0] # first row is ceo

    ceo = [0 if x == 'N/A' else x for x in ceo]
    data.loc[symbol, 'CEO Name'] = ceo[0]
    data.loc[symbol, 'CEO Year Born'] = int(ceo[4])

    div = soup.find('div', attrs={'class':'Mb(25px)'})
    info = div.findChildren("p" , recursive=False) # this div has two p children, left and right
    info = [child.get_text(strip=True, separator='\n').splitlines() for child in info]
    left = info[0]
    right = info[1]
    data.loc[symbol, 'Country'] = left[-3]
    if right[-1] != ':':
        data.loc[symbol, 'Employees'] = int(right[-1].replace(',', ''))
    else:
        data.loc[symbol, 'Employees'] = 0
'''
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
    statistics tab example: https://finance.yahoo.com/quote/TSLA/key-statistics?p=TSLA
'''
def read_statistics(data, symbol):
    # @TODO read statistics
    url = stock_tab_url('statistics', symbol)
    soup = get_page(url)

    rows = get_table_rows(soup, 1)
    # print(rows[0])
    # total cash
    # 52-Week Change

'''
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.
    holders tab example: https://finance.yahoo.com/quote/TSLA/holders?p=TSLA
'''
def read_blackrock(data, symbol):
    url = stock_tab_url('holders', symbol)
    soup = get_page(url)

    headers = get_table_header(soup, 1) # ['Holder', 'Shares', 'Date Reported', '% Out', 'Value']

    if len(soup.findAll('table')) < 1:
        return

    rows = get_table_rows(soup, 1) # was not working with table, some soups only have one table
    
    blackrock = None
    # find blackrock
    for row in rows:
        holder = row[0]
        if holder == 'Blackrock Inc.':
            blackrock = row
    
    # row = soup.findAll(string=re.compile('Blackrock Inc.'))[0].findPrevious()

    if blackrock:
         # casting
        # print(blackrock) # ['Blackrock Inc.', '171,860,959', 'Sep 29, 2022', '5.44%', '19,399,664,579']
        
        for x in [1, 4]:
            blackrock[x] = int(blackrock[x].replace(',', ''))
        blackrock[2] = datetime.strptime(blackrock[2], '%b %d, %Y')
        blackrock[3] = float(blackrock[3].strip('%'))/100

        for field, value in zip(headers[1:], blackrock[1:]):
            data.loc[symbol, field] = value
    # Shares
    # Date Reported
    # % Out
    # Value

def read_all_stocks(data, rows):
    ceos = list()
    count = 1
    for symbol, row in data.head(40).iterrows(): # @TODO change to read all data and not just head
        #print(symbol, row['Name'])
        name = row['Name']
        print(f'[{count}] reading {name}')
        read_profile(data, symbol)
        read_statistics(data, symbol)
        read_blackrock(data, symbol)
        count += 1

def pretty_sheet(title, data):
    pretty_table = tabulate(data.head(), headers = 'keys', tablefmt = 'pretty')
    lenght = len(pretty_table.splitlines()[0])
    title_formatted = title.center(lenght, '=')
    print(title_formatted)
    print(pretty_table)
    return title_formatted, pretty_table

def write_string(file, string_list):
    # open file in write mode
    with open(file, 'w') as fp:
        for item in string_list:
            # write each item on a new line
            #fp.write("%s\n" % item)
            fp.write(f'{item}\n')

def create_sheets(data):
    pretty_sheet(" all data ", data)

    # 5 stocks with most youngest CEOs
    title = ' 5 stocks with most youngest CEOs '
    table = data.nlargest(5, 'CEO Year Born')
    title, sheet = pretty_sheet(title, table[['Name', 'Country', 'Employees', 'CEO Name', 'CEO Year Born']])
    write_string(file_with_path('5stocks.txt'), [title, sheet])

    # 10 largest holds of Blackrock Inc
    title = ' 10 largest holds of Blackrock Inc '
    table = data.nlargest(10, 'Value')
    title, sheet = pretty_sheet(title, table[['Name', 'Shares', 'Date Reported', '% Out', 'Value']])
    write_string(file_with_path('blackrock.txt'), [title, sheet])

def count_url(base_url, count, offset):
    return f'{base_url}?count={count}&offset={offset}'

def scrape_yahoo_most_active(url):
    data = pd.DataFrame()
    count = 100
    offset = 0
    url_offset = count_url(url, count, offset)
    soup = get_page(url_offset)

    res_num = get_results_number(soup)
    print(f'reading {res_num} results')

    header = get_table_header(soup) # ['Symbol', 'Name', 'Price (Intraday)', 'Change', '% Change', 'Volume', 'Avg Vol (3 month)', 'Market Cap', 'PE Ratio (TTM)', '52 Week Range']

    rows = list()
    while offset <= res_num:
        url_offset = count_url(url, count, offset)
        soup = get_page(url_offset)
        rows += get_table_rows(soup)
        offset += count

    data = pd.DataFrame([row[:2] for row in rows], columns=['Code', 'Name'])
    data = data.set_index('Code')

    read_all_stocks(data, rows)
    return data

BASE_URL = 'https://finance.yahoo.com'
# url = 'https://finance.yahoo.com/most-active'
url = f'{BASE_URL}/most-active' 

scraping = True

filename = file_with_path('output.csv')
if scraping:
    data = scrape_yahoo_most_active(url)

    data = data.fillna(0)
    data.Employees = data.Employees.astype(int)
    data['CEO Year Born'] = data['CEO Year Born'].astype(int)

    create_sheets(data)
    data.head().to_csv(filename, sep='\t', encoding='utf-8', na_rep='NULL')
else:
    data = pd.read_csv(filename, sep='\t')
    create_sheets(data)