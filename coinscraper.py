import requests
import sqlite3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from decouple import config
import csv



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
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        coins = data['data']
        for coin in coins:
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





file = initialize()
write_to_csv(file)

