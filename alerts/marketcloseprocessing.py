import asyncio
from configparser import ConfigParser
import time
import aiohttp
import pandas as pd
import datetime

# read configs
api_parser = ConfigParser()
api_parser.read('../api.ini')
POLYGON_KEY = api_parser.get('APIs', 'polygon api key')

today = datetime.datetime.today().strftime("%Y-%m-%d")
yesterday = datetime.datetime.today() - datetime.timedelta(1)
yesterday = yesterday.strftime("%Y-%m-%d")
print(yesterday)
# import csv with index as ticker
df = pd.read_csv('stockslist.csv', index_col='ticker')
print(df['type'])
# remove all stock that is not common stock aka warrants and etfs
df = df[df['type'] == 'CS']


tickerlist = df.head(len(df)).index.to_list()

results = []

async def get(list):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url="https://api.polygon.io/v1/open-close/{}/{}?adjusted=true&apiKey={}".format(
                        list, today, POLYGON_KEY)) as response:
                reply = await response.json()
                if reply['status'] == 'OK':
                    results.append(reply)
    except Exception as e:
        print("Unable to get url {} due to {}.".format(list, e.__class__))


async def main(list):
    # print(list)
    all_responses = await asyncio.gather(*[get(url) for url in list])
    # print(all_responses)
    print("Finalized all. ret is a list of len {} outputs.".format(len(all_responses)))


start = time.time()
asyncio.get_event_loop().run_until_complete(main(tickerlist))
end = time.time()
df = pd.DataFrame.from_dict(results)
df = df.drop(['status', 'from'], axis=1)
df = pd.DataFrame.sort_values(df, by='symbol')
df.to_csv('gays.csv', index = None)