import json
import datetime
from requests import get
from sys import argv

def download_data(ticker:str) -> dict:
    """Function to download raw data from nasdaq API, returns a dictionary containing this data"""
    try:
        ticker = ticker.upper()
        now = datetime.datetime.now()
        today = now.date()
        start = str(today.replace(year=today.year - 5))
        base_url = "https://api.nasdaq.com"
        path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
        #Searched online for different headers to get a successful response from the api
        response = get(base_url + path, headers={'User-Agent' : 'Mozilla/5.0'})
        return response.json()
    except Exception as e:
        print(e)

def format_prices(prices: dict) -> list:
    """Function to extract a float value representing the closing price for each entry, returns a list of these floats"""
    #Extract closing prices
    closing_prices = []
    for entry in prices['data']['tradesTable']['rows']:
        closing_prices.append(entry['close']) 

    #Remove $ and convert to float for manipulation
    formatted_prices = []
    for entry in closing_prices:
        formatted_prices.append(float(entry.replace('$', '')))
    return formatted_prices

def get_medium(prices: list) -> float:
    """Function that returns the median value of a given list"""
    length = len(prices)
    sorted_prices = sorted(prices)

    #Odd case
    if length % 2 != 0:
        return sorted_prices[length // 2]
    
    #Even case
    else:
        avg = (sorted_prices[(length // 2) - 1] + sorted_prices[length // 2]) / 2
        return avg

def process_data(prices: list, ticker: str) -> dict:
    """Function to return a dictionary with formatted stock information from a list of closing prices"""
    data = {
        "min": min(prices),
        "max": max(prices),
        "avg": sum(prices) / len(prices),
        "medium": get_medium(prices),
        "ticker": ticker
    }
    return data

def fetch_stock_data(ticker: str) -> dict:
    """Helper function to execute other functions given a ticker symbol"""
    data = process_data(format_prices(download_data(ticker)), ticker)
    return data

ticker_list = []

for i in range(1, len(argv)):
    if len(argv) < 1:
        print("No ticker symbols detected!!!")
    else:
        ticker_list.append(argv[i])

data = []

for i in range(0, len(ticker_list)):
     data.append(fetch_stock_data(ticker_list[i]))

#./file_directory
with open("stocks.json", "w") as outfile:
    json.dump(data, outfile, indent = 4)
