import asyncio
import csv

import aiohttp
import time

from configparser import ConfigParser

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
                    url="https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/{}?&apiKey={}".format(
                        list[0])) as response:
                gays = await response.json()
                # df = await polygon.agg_df('GME', 'minute', "30", ((dt.datetime.now() - dt.timedelta(
                # days=7)).strftime("%Y-%m-%d")), dt.datetime.now().strftime("%Y-%m-%d"), POLYGON_KEY)=

                if gays['ticker']['day']['vw']<20:
                    print(list[0])
                    yeet.append(list[0])







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
print(yeet)