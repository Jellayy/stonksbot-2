import asyncio
import csv

import aiohttp
import time

from configparser import ConfigParser

import pandas as pd
from pandas import read_csv

parser = ConfigParser()
parser.read('../config.ini')
MONITORED_STOCKS = parser.get('General', 'monitored stocks').split(",")
api_parser = ConfigParser()
api_parser.read('../api.ini')
POLYGON_KEY = api_parser.get('APIs', 'polygon api key')

with open('stockslist.csv', newline='') as f:
    reader = csv.reader(f)
    stock_list = list(reader)

yeet = []


async def get(list):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url="https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/2021-09-13/2021-09-13?adjusted=true&sort=asc&limit=50000&apiKey={}".format(
                        list[0], POLYGON_KEY)) as response:
                data = await response.json()

                df = pd.DataFrame(data['results'])
                average = df['vw'].mean()
                biggestchange = ((df['h'] - df['l']) / df['o']).max()
                gays = [list[0], biggestchange]
                yeet.append(gays)



    except Exception as e:
        print("Unable to get url {} due to {}.".format(list, e.__class__))


async def main(list):
    # print(list)
    all_responses = await asyncio.gather(*[get(url) for url in list])
    # print(all_responses)
    print("Finalized all. ret is a list of len {} outputs.".format(len(all_responses)))


# urls = websites.split("\n")
# print(ticker_list)
num_urls = len(stock_list)

start = time.time()
asyncio.get_event_loop().run_until_complete(main(stock_list))
end = time.time()

print("Took {} seconds to pull {} websites.".format(end - start, num_urls))
print(len(yeet))
yeet.sort(key=lambda i: i[1])
print(yeet)
df = pd.DataFrame(yeet)
df.to_csv('processed.csv', index=False, header=0)
