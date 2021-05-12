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

            #append each coin data to a list
            newdata=[]
            newdata.append(coin['name'])
            newdata.append(coin['symbol'])
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

#Writing to CSV file from the data gathered
def write_to_csv(file):

    fields = ['Name', 'Symbol', 'Percent Change', 'Percent Change 7 days', 'Market Cap', 'Volume 24 Hr', 'Circulating Supply', 'Pull Time']
    filename = 'coinmarketcap.csv'

    #removes the pull time since csv doesn't need that.
    # newfile = file[:len(file)

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
                (PULLTIME DATETIME, Name TEXT, PER_CHANGE_H TEXT, PER_CHANGE_D TEXT, 
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
            market.append(i[len(i)-1])
            market.append(i[0])
            market.append(i[2])
            market.append(i[3])
            market.append(i[4])
            market.append(i[5])
            market.append(i[6])
            #append tuple to list
            marketdata.append(tuple(market))

        # print(marketdata)

        #Insert Data into Market Data table
        market_insert_query = """INSERT INTO MARKETDATA (PULLTIME , Name , PER_CHANGE_H , PER_CHANGE_D , 
                MARKET_CAP , VOL_H , CIRCULATING_SUPPLY ) VALUES (?, ?,?,?,?,?,?) """
        c.executemany(market_insert_query, marketdata)
        conn.commit()

        
        #List all data from MARKET DATA TABLE
        c.execute("SELECT * FROM MARKETDATA")
        row = c.fetchall()
        print(row)
        
    except Error as e:
        print(e)
    

    
#Call the 3 functions
file = initialize()
write_to_csv(file)
connect_db(file)





