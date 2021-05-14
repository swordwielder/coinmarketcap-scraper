# Coin Market Cap Scraper

## INTRODUCTION
This is a Coin Market Cap Scraper that scrapes the top 100 coins on coinmarketcap.com of the following information

* CryptoCurrency name & Symbol

* Price

* 24h % (This is the change in price)

* 7d % (This is the change in price)

* Market Cap

* Volume (24h)

* Circulating Supply


## What it does

**Scrapes the information listed above and put it in an csv file including the scrape time**

### Additional Feature

* Put all the information gathered into a sqlite database including the scape time


## Requirements:

* ```pip install -r requirements.txt```

* Google Chrome installed 


#### Optional
* Request for a API Key from [here](https://coinmarketcap.com/api/) and put the key in a `.env` file with the name API_KEY='YOUR_API_KEY_HERE' (ex: API_KEY=fuywge83hf7832j) in the same directory (Will run faster if choose to use API)

* [SQLite Studio](https://sqlitestudio.pl/) **optional** can be used to view the data from the database 


## To run:

* ```python coinscraper.py```

## Result:

**You should see two files**

* coinmarketcap.csv

* crypto.db


## Resources:

* [coin market cap](https://coinmarketcap.com/) 

* [coin market cap api](https://coinmarketcap.com/api/) (300 per day, 10,000 per month)


## Library/frameworks:

* Python

* BeautifulSoup

* Selenium

* requests

* decouple

* sqlite


## Author:

[Qi](https://github.com/swordwielder/discordStockBot/graphs/contributors) - [LinkedIn](https://www.linkedin.com/in/qifchen/)
