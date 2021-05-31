import discord
from discord.ext import commands, tasks
import datetime as dt
from configparser import ConfigParser
from itertools import cycle
import yfinance as yf
from operator import itemgetter
import utils.embeds as embeds


# Read config.ini
parser = ConfigParser()
parser.read('config.ini')
DISCORD_KEY = parser.get('APIs', 'discord.py api key')
POLYGON_KEY = parser.get('APIs', 'polygon api key')
PREFIX = parser.get('General', 'command prefix') + " "
MONITORED_STOCKS = parser.get('General', 'monitored stocks').split(",")
STOCK_CYCLE = cycle(MONITORED_STOCKS)
STATUS_UPDATE_TIMER = parser.getint('Misc', 'status update timer (seconds)')
ALERT_CHANNEL = parser.get('General', 'alert channel')
ALERT_ROLE = parser.get('General', 'alert role id')


client = commands.Bot(command_prefix=PREFIX)


# Run on login
@client.event
async def on_ready():
    print(f'[{dt.datetime.now().time().strftime("%H:%M:%S")}] Logged in as {client.user}')
    update_status.start()
    moon_alert.start()
    daily_summary.start()


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


# Send alerts to users if a monitored stock begins to moon (or go into the ground lmao)
@tasks.loop(minutes=5)
async def moon_alert():
    if dt.datetime.now().isoweekday() in range(1, 6):
        if dt.time(1) <= dt.datetime.now().time() <= dt.time(17):
            global MONITORED_STOCKS
            global ALERT_ROLE
            global ALERT_CHANNEL
            for stock_name in MONITORED_STOCKS:
                stock = yf.Ticker(stock_name)
                previous = stock.history(period='1d', interval='1m', prepost='True', actions='False').iloc[-6]['Close']
                now = stock.history(period='1d', interval='1m', prepost='True', actions='False').iloc[-1]['Close']
                percent_change = round(((now - previous) / previous) * 100, 2)
                five_min_dif = round(now - previous, 2)
                if percent_change >= 3:
                    for guild in client.guilds:
                        for channel in guild.channels:
                            if str(channel) == ALERT_CHANNEL:
                                await channel.send(f'{stock_name} **+${five_min_dif}** | **+{percent_change}%** last 5 min \n <@&{ALERT_ROLE}>')
                                print(f'[{dt.datetime.now().time().strftime("%H:%M:%S")}] Task: Moon Alert: {stock_name} {percent_change} 5min upward trend triggered')
                elif percent_change <= -3:
                    for guild in client.guilds:
                        for channel in guild.channels:
                            if str(channel) == ALERT_CHANNEL:
                                await channel.send(f'{stock_name} **${five_min_dif}** | **+{percent_change}%** last 5 min \n <@&{ALERT_ROLE}>')
                                print(f'[{dt.datetime.now().time().strftime("%H:%M:%S")}] Task: Moon Alert: {stock_name} {percent_change} 5min downward trend triggered')
                else:
                    print(f'[{dt.datetime.now().time().strftime("%H:%M:%S")}] Task: Moon Alert: No {stock_name} Trend Detected')


@tasks.loop(hours=1)
async def daily_summary():
    if dt.datetime.now().isoweekday() in range(1, 6):
        if dt.time(17) <= dt.datetime.now().time() <= dt.time(18):
            global MONITORED_STOCKS
            today_change = []
            for stock_name in MONITORED_STOCKS:
                stock = yf.Ticker(stock_name)
                data = stock.history(interval='1d', period='1d')
                open_price = data['Open'][0]
                close_price = data['Close'][0]
                delta = round(close_price - open_price, 2)
                percent_change = round(((close_price - open_price) / open_price) * 100, 2)
                today_change.append([stock_name, delta, percent_change, abs(percent_change)])
            today_change_sorted = sorted(today_change, key=itemgetter(3))
            today_change_sorted.reverse()
            print(today_change_sorted)
            for guild in client.guilds:
                for channel in guild.channels:
                    if str(channel) == ALERT_CHANNEL:
                        await channel.send(embed=await embeds.daily_summary(client, today_change_sorted))



# Init call to discord API (Nothing below this)
client.run(DISCORD_KEY)
