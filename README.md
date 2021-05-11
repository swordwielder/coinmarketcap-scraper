# Coin Market Cap Scraper

## INTRODUCTION
This is a Coin Market Cap Scrape that scrapes the top 100 coins of the following information

* CryptoCurrency name

* Price

* 24h % (This is the change in price)

* 7d % (This is the change in price)

* Market Cap

* Volume (24h)

* Circulating Supply

## What it does

**Scrapes the information listed above and put it in an csv file**

* Will add feature for sql inject

## Requirements:
* ```pip install requirements.txt```
* Request for a API Key from [here](https://coinmarketcap.com/api/) and put the key in a '.env' file with the name API_KEY='YOURKEYHERE'

## To run:

* ```python coinscraper.py```


## Resources:

* [coin market cap](https://coinmarketcap.com/) 

* [coin market cap api](https://coinmarketcap.com/api/) (300 per day, 10,000 per month)




## Library/frameworks:

* Python

* requests

* decouple

* sqlite

## Author:

[Qi](https://github.com/swordwielder/discordStockBot/graphs/contributors) - [LinkedIn](https://www.linkedin.com/in/qifchen/)
