import discord
from discord.ext import commands
import mplfinance as mpf
import pandas_datareader.data as web
import datetime as dt
import embeds
import VERY_SECRET_LAUNCH_CODES
import api as nyse

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
async def stonk(ctx, stock=None, start='2021-1-1', end='2021-3-12'):
    if stock is None:
        await ctx.channel.send(embed=await embeds.stonk_syntax_error(client))
    else:
        start = dt.datetime.strptime(start, '%Y-%m-%d')
        end = dt.datetime.strptime(end, '%Y-%m-%d')

        df = web.DataReader(stock, 'yahoo', start, end)
        # TODO: fix date handling between these functions
        # df = await nyse.get_polygon_dataframe("GME", "2021-03-07", "2021-03-14")

        mpf.plot(df, type='candle', volume=True, style='mike', savefig='plot.png')
        file = discord.File('plot.png', filename="plot.png")
        await ctx.channel.send(file=file)


client.run(VERY_SECRET_LAUNCH_CODES.US_LAUNCH_CODE())
