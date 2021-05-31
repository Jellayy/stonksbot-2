import discord
from discord.ext import commands, tasks
import datetime as dt
from configparser import ConfigParser
from itertools import cycle
import yfinance as yf


# Read config.ini
parser = ConfigParser()
parser.read('config.ini')
DISCORD_KEY = parser.get('APIs', 'discord.py api key')
PREFIX = parser.get('General', 'command prefix') + " "
MONITORED_STOCKS = parser.get('General', 'monitored stocks').split(",")
STOCK_CYCLE = cycle(MONITORED_STOCKS)
STATUS_UPDATE_TIMER = parser.getint('Misc', 'status update timer (seconds)')


client = commands.Bot(command_prefix=PREFIX)


# Run on login
@client.event
async def on_ready():
    print(f'[{dt.datetime.now().time().strftime("%H:%M:%S")}] Logged in as {client.user}')
    update_status.start()


# Update bot status with the price of a monitored stock
@tasks.loop(seconds=STATUS_UPDATE_TIMER)
async def update_status():
    global STOCK_CYCLE
    try:
        stock_name = next(STOCK_CYCLE)
        stock = yf.Ticker(stock_name)
        price = round(stock.history(period='1d', interval='1m', prepost='True', actions='False').iloc[-1]['Close'], 2)
        await client.change_presence(activity=discord.Activity(name=f"{stock_name}: ${price}", type=3))
        print(f'[{dt.datetime.now().time().strftime("%H:%M:%S")}] Task: Update Status: {stock_name}: ${price}')
    except RuntimeError:
        await client.change_presence(activity=discord.Activity(name="yfinance API down", type=3))
        print(f'[{dt.datetime.now().time().strftime("%H:%M:%S")}] Task ERROR: Update Status: yfinance API down')


# Init call to discord API (Nothing below this)
client.run(DISCORD_KEY)
