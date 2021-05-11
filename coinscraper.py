import requests
import sqlite3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from decouple import config


API_KEY = config('API_KEY')


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'3',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY,
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print('Actual Data')
    # print(data)
    print(data['data'])
    coins = data['data']
    for coin in coins:
        print('Name: '+coin['name'])
        print('Symbol: ' + coin['symbol'])
        print('Percent Change: ' + str(coin['quote']['USD']['percent_change_24h']))
        print('Percent change 7 days: '+ str(coin['quote']['USD']['percent_change_7d']))
        print('Market cap: ' + str(coin['quote']['USD']['market_cap']))
        print('Volume 24 hours: '+ str(coin['quote']['USD']['volume_24h']))
        print('Circulating Supply: '+ str(coin['circulating_supply']))
        print()
    # coin_json = json.dumps(data, indent=4, sort_keys=True)
    # print(coin_json)
    # print('For each item')
    # for i in coin_json:
    #     print(i['data'])

#   print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)



