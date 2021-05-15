import requests
import sqlite3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from decouple import config
import csv
import sqlite3
from sqlite3 import Error
from datetime import datetime
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import selenium as se
from lxml import html
import xlwt 
from xlwt import Workbook 
import csv
import warnings
import lxml
from lxml import html
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from lxml import etree
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
#API call method
#initialize function
def initialize():

    alldata = []
    #gets API key from environment variable
    API_KEY = config('API_KEY')

    # sets url and parameters and takes API key for header
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'100',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
    }

    #initialize a session and update header for session
    session = Session()
    session.headers.update(headers)

    try:
        #get response from the url
        response = session.get(url, params=parameters)
        #loads it in json for all the text found from response
        data = json.loads(response.text)
        #set all coins to the data 
        coins = data['data']
        #for each coin in all the coins found
        for coin in coins:
            # print(coin)
            #append each coin data to a list
            newdata=[]
            newdata.append(coin['name'])
            newdata.append(coin['symbol'])
            newdata.append(coin['quote']['USD']['price'])
            newdata.append(str(coin['quote']['USD']['percent_change_24h']))
            newdata.append(coin['quote']['USD']['percent_change_7d'])
            newdata.append(coin['quote']['USD']['market_cap'])
            newdata.append(coin['quote']['USD']['volume_24h'])
            newdata.append(coin['circulating_supply'])

            # datetime object containing current date and time
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            newdata.append(dt_string)

            #append the single coin
            alldata.append(newdata)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return alldata





#BeautifulSoup Scraping method

def start_chrome():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    # browser = webdriver.Chrome()
    url = "https://coinmarketcap.com/"
    browser.get(url) #navigate to the page
    
    #maximize the window (not really necessary but just waited to)
    browser.maximize_window()
    
    wait = WebDriverWait(browser, 2)
    #Search for every 20th element in the Table row
    men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/table/tbody/tr[20]')))                                      
    ActionChains(browser).move_to_element(men_menu).perform()
    # wait for element to appear, then hover it

    #Repeat the process 4 more times.
    men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/table/tbody/tr[40]')))
    ActionChains(browser).move_to_element(men_menu).perform()
    
    men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/table/tbody/tr[60]')))
    ActionChains(browser).move_to_element(men_menu).perform()
    
    men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/table/tbody/tr[80]')))
    ActionChains(browser).move_to_element(men_menu).perform()
    
    men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/table/tbody/tr[100]')))
    ActionChains(browser).move_to_element(men_menu).perform()
    

    innerHTML = browser.execute_script("return document.body.innerHTML")

    return innerHTML


def scrape(r):

    
    # r = requests.get('https://coinmarketcap.com/')
    # print(r.content)

    
    # soup = BeautifulSoup(r.content, "lxml")
    soup = BeautifulSoup(r,features="lxml")
    
    alldata = []
    coins = soup.find_all('tr')
    for coin in range(1,len(coins)):
        temp = coins[coin].findAll(text=True)
        # print('THIS IS THE TEMP')
        print(temp)
        newdata = []
        if len(temp)==16:
            newdata.append(temp[1])
            newdata.append(temp[3])
            newdata.append(temp[4])
            newdata.append(temp[6]+temp[8])
            newdata.append(temp[9]+temp[11])
            newdata.append(temp[12])
            newdata.append(temp[13])
            a = temp[15].split()
            newdata.append(a[0])
        if len(temp)==11:
            newdata.append(temp[1])
            newdata.append(temp[3])
            newdata.append(temp[4])
            newdata.append(temp[5])
            newdata.append(temp[6])
            newdata.append(temp[7])
            newdata.append(temp[8])
            a=temp[10].split()
            newdata.append(a[0])


        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        newdata.append(dt_string)
        alldata.append(newdata)
        # print()
        # print("ALL THE DATA")
        # print(alldata)
        
    return alldata
            





#Writing to CSV file from the data gathered
def write_to_csv(file):

    fields = ['Name', 'Symbol', 'Price', 'Percent Change', 'Percent Change 7 days', 'Market Cap', 'Volume 24 Hr', 'Circulating Supply', 'Pull Time']
    filename = 'coinmarketcap.csv'


    #Writes the info pulled into the CSV
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(file)



#Creates the db, create table and insert.
def connect_db(alldata):

    try:
        conn = sqlite3.connect('crypto.db')  # You can create a new database by changing the name within the quotes
        c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

        #create table query and execute
        c.execute('''CREATE TABLE  IF NOT EXISTS CRYPTOCURRENCIES
                (Name TEXT PRIMARY KEY, Symbol TEXT)''')

        #Create table query and execute
        c.execute('''CREATE TABLE  IF NOT EXISTS MARKETDATA
                (PULLTIME DATETIME, Name TEXT, Price TEXT, PER_CHANGE_H TEXT, PER_CHANGE_D TEXT, 
                MARKET_CAP TEXT, VOL_H TEXT, CIRCULATING_SUPPLY TEXT, FOREIGN KEY (Name) REFERENCES CRYPTOCURRENCIES(Name) ) ''')

        #Crypto Name and Symbol list
        crytoNS = []
        for i in alldata:
            crytoNS.append(tuple(i[:2]))
        
        #Insert that list of tuples into the database and commit
        crypto_insert_query = """INSERT OR REPLACE INTO CRYPTOCURRENCIES (Name, Symbol) VALUES (?, ?) """
        c.executemany(crypto_insert_query, crytoNS)
        conn.commit()

        #MarketData List
        marketdata = []        
        #Add data for each row to append to a tuple
        for i in alldata:
            market = []
            market.append(i[8])
            market.append(i[0])
            market.append(i[2])
            market.append(i[3])
            market.append(i[4])
            market.append(i[5])
            market.append(i[6])
            market.append(i[7])
            #append tuple to list
            marketdata.append(tuple(market))


        #Insert Data into Market Data table
        market_insert_query = """INSERT INTO MARKETDATA (PULLTIME , Name , Price, PER_CHANGE_H , PER_CHANGE_D , 
                MARKET_CAP , VOL_H , CIRCULATING_SUPPLY ) VALUES (?, ?,?,?,?,?,?,?) """
        c.executemany(market_insert_query, marketdata)
        conn.commit()

        
        #List all data from MARKET DATA TABLE
        c.execute("SELECT * FROM MARKETDATA")
        row = c.fetchall()
        # print(row)
        
    except Error as e:
        print(e)
    

    


#Call the 3 functions
# file = initialize()
# print('THIS IS THE API call data')
# print(file)
# write_to_csv(file)
# connect_db(file)
# print()
page_data = start_chrome()
coindatalist = scrape(page_data)


write_to_csv(coindatalist)
connect_db(coindatalist)