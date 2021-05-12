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