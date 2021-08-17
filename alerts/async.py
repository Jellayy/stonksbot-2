import asyncio
import aiohttp
import time
from urls import websites
import utils.polygon as polygon
from configparser import ConfigParser
import datetime as dt
import pandas as pd
import pytz
from datetime import datetime

parser = ConfigParser()
parser.read('../config.ini')
MONITORED_STOCKS = parser.get('General', 'monitored stocks').split(",")
api_parser = ConfigParser()
api_parser.read('../api.ini')
POLYGON_KEY = api_parser.get('APIs', 'polygon api key')


async def get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                gays = await response.json()
                # df = await polygon.agg_df('GME', 'minute', "30", ((dt.datetime.now() - dt.timedelta(
                # days=7)).strftime("%Y-%m-%d")), dt.datetime.now().strftime("%Y-%m-%d"), POLYGON_KEY)

                df = pd.DataFrame(gays['results'])
                est = pytz.timezone('US/Eastern')
                utc = pytz.utc
                df.index = [datetime.utcfromtimestamp(ts / 1000.).replace(tzinfo=utc).astimezone(est) for ts in df['t']]
                df.index.name = 'Date'
                df.columns = ['Volume', 'Volume Weighted', 'Open', 'Close', 'High', 'Low', 'Time', 'Num Items']

    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def main(urls):
    all_responses = await asyncio.gather(*[get(url) for url in urls])
    print("Finalized all. ret is a list of len {} outputs.".format(len(all_responses)))


urls = websites.split("\n")
num_urls = len(urls)

start = time.time()
asyncio.get_event_loop().run_until_complete(main(urls))
end = time.time()

print("Took {} seconds to pull {} websites.".format(end - start, num_urls))
