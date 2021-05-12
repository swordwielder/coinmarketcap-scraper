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
# import TestDB.db

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   password="yourpassword"
# )

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

            # datetime object containing current date and time
            now = datetime.now()
            # print("now =", now)
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            # print("date and time =", dt_string)
            newdata.append(dt_string)


            alldata.append(newdata)

            


    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return alldata

#Writing to CSV file from the data gathered
def write_to_csv(file):

    fields = ['Name', 'Symbol', 'Percent Change', 'Percent Change 7 days', 'Market Cap', 'Volume 24 Hr', 'Circulating Supply', 'Time']
    filename = 'coinmarketcap.csv'

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(file)



def connect_db(alldata):
    try:
        conn = sqlite3.connect('crypto.db')  # You can create a new database by changing the name within the quotes
        c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
        c.execute('''CREATE TABLE  IF NOT EXISTS CRYPTOCURRENCIES
                (Name TEXT PRIMARY KEY, Symbol TEXT)''')

        c.execute('''CREATE TABLE  IF NOT EXISTS MARKETDATA
                (PULLTIME DATETIME, Name TEXT, PER_CHANGE_H TEXT, PER_CHANGE_D TEXT, 
                MARKET_CAP TEXT, VOL_H TEXT, CIRCULATING_SUPPLY TEXT, FOREIGN KEY (Name) REFERENCES CRYPTOCURRENCIES(Symbol) ) ''')

        crytoNS = []
        for i in alldata:
            crytoNS.append(tuple(i[:2]))
        

        sqlite_insert_query = """INSERT INTO CRYPTOCURRENCIES (Name, Symbol) VALUES (?, ?) """
        c.executemany(sqlite_insert_query, crytoNS)
        conn.commit()
        
        
        c.execute("SELECT * FROM CRYPTOCURRENCIES")
        row = c.fetchall()
        print(row)
        
    except Error as e:
        print(e)
    
    # return conn

# def create_table(conn):
    
file = initialize()
# write_to_csv(file)

connect_db(file)





