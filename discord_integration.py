import discord
from discord.ext import commands
import mplfinance as mpf
import pandas as pd
import pytz
from datetime import datetime
import requests
import embeds
import VERY_SECRET_LAUNCH_CODES

client = commands.Bot(command_prefix='gib ')


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


# This looks terrible because making the bot use code blocks is disgusting, I will never use this again
@client.command()
async def ping(ctx):
    await ctx.send(f"""
```
Latency: {round(client.latency*1000, 3)}ms
```
""")


# This was made in like 2 hours for testing but it works ez clap
@client.command()
async def stonk(ctx, stock=None, timespan='day', multiplier=int(1), start='2021-01-01', end=datetime.today().strftime("%Y-%m-%d")):
    if stock is None:
        await ctx.channel.send(embed=await embeds.stonk_syntax_error(client))
    else:
        r = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{stock.upper()}/range/{multiplier}/{timespan}/{start}/{end}?apiKey={VERY_SECRET_LAUNCH_CODES.HYDROGEN_LAUNCH_CODE()}')

        try:
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

            saving_params = dict(fname='plot.png', dpi=1200)
            mpf.plot(df, type='candle', volume=True, style=s, savefig=saving_params)
            file = discord.File('plot.png', filename="plot.png")
            await ctx.channel.send(file=file, embed=await embeds.stonk_view(client, stock.upper()))
        except KeyError:
            await ctx.channel.send(embed=await embeds.stonk_syntax_error(client))

client.run(VERY_SECRET_LAUNCH_CODES.PLUTONIUM_LAUNCH_CODE())
