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
from apicall import initialize   





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
    
    # soup = BeautifulSoup(r.content, "lxml")
    soup = BeautifulSoup(r,features="lxml")
    alldata = []
    #Finds all the table row on the page
    coins = soup.find_all('tr')
    for coin in range(1,len(coins)):
        temp = coins[coin].findAll(text=True)  #Only gets the text
        
        newdata = []
        while ' ' in temp: 
            temp.remove(' ')
        
        if 'Buy' in temp:
            temp.remove('Buy')

        print(temp)
        #Add each individual info of the scraped data
        newdata.append(temp[1])
        newdata.append(temp[3])
        newdata.append(temp[4])
        if len(temp)==13:
            newdata.append(temp[5]+temp[6])
            newdata.append(temp[7]+temp[8])
            newdata.append(temp[9])
            newdata.append(temp[10])
        if len(temp)==11:
            newdata.append(temp[5])
            newdata.append(temp[6])
            newdata.append(temp[7])
            newdata.append(temp[8])
        
        a=temp[len(temp)-1].split()
        newdata.append(a[0])
        #Gets the current time and then append that to the list
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        newdata.append(dt_string)
        alldata.append(newdata)
        
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
        conn.close()
        
        
    except Error as e:
        print(e)
    


#Call the Web scraper method then write to csv and connect and write to database
page_data = start_chrome()
coindatalist = scrape(page_data)
write_to_csv(coindatalist)
connect_db(coindatalist)



#Call the functions for API scrape, comment out the 3 lines below to use the API method
# file = initialize()
# write_to_csv(file)
# connect_db(file)
