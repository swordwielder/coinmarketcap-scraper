import requests
import sqlite3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from decouple import config
import csv
import sqlite3
from sqlite3 import Error


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
            #append each coin to the list
            newdata=[]
            newdata.append(coin['name'])
            newdata.append(coin['symbol'])
            newdata.append(str(coin['quote']['USD']['percent_change_24h']))
            newdata.append(coin['quote']['USD']['percent_change_7d'])
            newdata.append(coin['quote']['USD']['market_cap'])
            newdata.append(coin['quote']['USD']['volume_24h'])
            newdata.append(coin['circulating_supply'])
            alldata.append(newdata)
        

    #   print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return alldata

#Writing to CSV file from the data gathered
def write_to_csv(file):

    fields = ['Name', 'Symbol', 'Percent Change', 'Percent Change 7 days', 'Market Cap', 'Volume 24 Hr', 'Circulating Supply']
    filename = 'coinmarketcap.csv'

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(file)



def connect_db():
    conn = sqlite3.connect('TestDB.db')  # You can create a new database by changing the name within the quotes
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
    c.execute('''CREATE TABLE  IF NOT EXISTS CRYPTOCURRENCIES
             (Name TEXT, Symbol TEXT PRIMARY KEY)''')

    c.execute('''CREATE TABLE  IF NOT EXISTS MARKETDATA
             (PULLTIME DATETIME, Symbol TEXT, PER_CHANGE_H TEXT, PER_CHANGE_D TEXT, 
             MARKET_CAP TEXT, VOL_H TEXT, CIRCULATING_SUPPLY TEXT, FOREIGN KEY (Symbol) REFERENCES CRYPTOCURRENCIES(Symbol) ) ''')
          
    

connect_db()


file = initialize()
write_to_csv(file)

