import requests
import pandas as pd
import pytz
from datetime import datetime
import mplfinance as mpf
import VERY_SECRET_LAUNCH_CODES


def gen_graph(stock, timespan, multiplier, start, end):
    r = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{stock.upper()}/range/{multiplier}/{timespan}/{start}/{end}?apiKey={VERY_SECRET_LAUNCH_CODES.HYDROGEN_LAUNCH_CODE()}')

    # Copy pasted code to format dataframe for mplfinance
    df = pd.DataFrame(r.json()['results'])
    est = pytz.timezone('US/Eastern')
    utc = pytz.utc
    df.index = [datetime.utcfromtimestamp(ts / 1000.).replace(tzinfo=utc).astimezone(est) for ts in df['t']]
    df.index.name = 'Date'
    df.columns = ['Volume', 'Volume Weighted', 'Open', 'Close', 'High', 'Low', 'Time', 'Num Items']

    # Very dank custom mpl theme copyright your mom LLC
    mc = mpf.make_marketcolors(up='#00a320', down='#ff3334', inherit=True)
    s = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc, gridaxis='horizontal', gridcolor='#454545', gridstyle='solid', edgecolor='#454545', facecolor='#000000')

    # Saves graph
    saving_params = dict(fname='plot.png', dpi=1200)
    mpf.plot(df, type='candle', volume=True, style=s, savefig=saving_params, vlines=dict(vlines=['2021-03-18 09:30', '2021-03-18 16:00'], linewidths=0.2, colors="#454545"))
