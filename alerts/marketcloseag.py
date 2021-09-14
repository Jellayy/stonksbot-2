import asyncio
import csv
import aiohttp
import time
from configparser import ConfigParser
import requests
import pandas as pd

# load config keys with config parser as POLYGON_KEY
api_parser = ConfigParser()
api_parser.read('../api.ini')
POLYGON_KEY = api_parser.get('APIs', 'polygon api key')

# get list of all traded stocks
ticker_list = []
# Create polygon request string
r = requests.get(
    f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&sort=ticker&order=asc&limit=1000&apiKey={POLYGON_KEY}")
while r.json().get("next_url"):
    for i in r.json()["results"]:
        ticker_list.append(i)
    r = requests.get(r.json()["next_url"] + f"&apiKey={POLYGON_KEY}")
# append all tickers to list
for i in r.json()["results"]:
    ticker_list.append(i)

print(len(ticker_list))
print(ticker_list[0])

df = pd.DataFrame(ticker_list)
df.to_csv('stockslist.csv', index = None)
