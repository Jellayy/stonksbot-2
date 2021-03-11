import discord
from discord.ext import commands
import mplfinance as mpf
import pandas_datareader.data as web
import datetime as dt
import VERY_SECRET_LAUNCH_CODES

client = commands.Bot(command_prefix='gib ')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


# This was made in like 2 hours for testing but it works ez clap
@client.command()
async def stonk(ctx, stock=None, start='2021-1-1', end='2021-3-11'):
    if stock is None:
        return
    else:
        start = dt.datetime.strptime(start, '%Y-%m-%d')
        end = dt.datetime.strptime(end, '%Y-%m-%d')
        df = web.DataReader(stock, 'yahoo', start, end)
        mpf.plot(df, type='candle', volume=True, style='mike', savefig='plot.png')
        file = discord.File('plot.png', filename="plot.png")
        await ctx.channel.send(file=file)


client.run(VERY_SECRET_LAUNCH_CODES.US_LAUNCH_CODE())
