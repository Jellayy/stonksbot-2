import requests
import pandas as pd
import pytz
from datetime import datetime


# Polygon.io gives aggregate bar results in JSON for some reason, this converts them to a pandas dataframe
def agg_df(symbol, timespan, multiplier, start, end, key):
    r = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{start}/{end}?unadjusted=false&sort=asc&limit=50000&apiKey={key}')

    df = pd.DataFrame(r.json()['results'])
    if 'a' in df.columns:
        df = df.drop(columns=["a"])
    if 'op' in df.columns:
        df = df.drop(columns=["op"])
    est = pytz.timezone('US/Eastern')
    utc = pytz.utc
    df.index = [datetime.utcfromtimestamp(ts / 1000.).replace(tzinfo=utc).astimezone(est) for ts in df['t']]
    df.index.name = 'Date'
    df.columns = ['Volume', 'Volume Weighted', 'Open', 'Close', 'High', 'Low', 'Time', 'Num Items']

    return df


def info(symbol, key):
    r = requests.get(f'https://api.polygon.io/v1/meta/symbols/{symbol}/company?&apiKey={key}')

    return r.json()
