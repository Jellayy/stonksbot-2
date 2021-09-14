import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import datetime as dt
from configparser import ConfigParser
from itertools import cycle
from operator import itemgetter
import utils.embeds as embeds
import utils.graphs as graphs
import utils.polygon as polygon


########################################################################################################################
#                                                   Config Loading                                                     #
########################################################################################################################
# Base config
parser = ConfigParser()
parser.read('config.ini')
PREFIX = parser.get('General', 'command prefix') + " "
MONITORED_STOCKS = parser.get('General', 'monitored stocks').split(",")
STATUSBAR_STOCKS = parser.get('General', 'statusbar stocks').split(",")
STOCK_CYCLE = cycle(STATUSBAR_STOCKS)
STATUS_UPDATE_TIMER = parser.getint('Misc', 'status update timer (seconds)')
ALERT_CHANNEL = parser.get('General', 'alert channel')
ALERT_ROLE = parser.get('General', 'alert role id')
DEBUG_CHANNEL = parser.get('Developer Settings', 'debug channel')

# API config
api_parser = ConfigParser()
api_parser.read('api.ini')
DISCORD_KEY = api_parser.get('APIs', 'discord.py api key')
POLYGON_KEY = api_parser.get('APIs', 'polygon api key')


########################################################################################################################
#                                                      Bot Init                                                        #
########################################################################################################################
# Init bot with slash commands
client = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)


# Run on login
@client.event
async def on_ready():
    print(f'[{dt.datetime.now().time().strftime("%H:%M:%S")}] Logged in as {client.user}')
    update_status.start()
    moon_alert.start()
    # daily_summary.start()


########################################################################################################################
#                                                        Tasks                                                         #
########################################################################################################################
# Update bot status with the price of a monitored stock
@tasks.loop(seconds=STATUS_UPDATE_TIMER)
async def update_status():
    global STOCK_CYCLE
    try:
        stock_name = next(STOCK_CYCLE)
        price = round(polygon.agg_df(stock_name, 'day', '1', dt.datetime.now().strftime("%Y-%m-%d"), dt.datetime.now().strftime("%Y-%m-%d"), POLYGON_KEY)['Close'][0], 2)
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
                try:
                    candle = polygon.agg_df(stock_name, 'minute', '5', dt.datetime.now().strftime("%Y-%m-%d"), dt.datetime.now().strftime("%Y-%m-%d"), POLYGON_KEY)
                    previous = candle['Open'][-1]
                    now = candle['Close'][-1]
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
                except Exception as e:
                    for guild in client.guilds:
                        for channel in guild.channels:
                            if str(channel) == DEBUG_CHANNEL:
                                await channel.send(f'{stock_name} {repr(e)}')


# Send Brief daily summary of monitored stocks
@tasks.loop(hours=1)
async def daily_summary():
    if dt.datetime.now().isoweekday() in range(1, 6):
        if dt.time(17) <= dt.datetime.now().time() <= dt.time(18):
            global MONITORED_STOCKS
            today_change = []
            for stock_name in MONITORED_STOCKS:
                data = polygon.agg_df(stock_name, 'day', '1', dt.datetime.now().strftime("%Y-%m-%d"), dt.datetime.now().strftime("%Y-%m-%d"), POLYGON_KEY)
                open_price = data['Open'][0]
                close_price = data['Close'][-1]
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


########################################################################################################################
#                                                      Commands                                                        #
########################################################################################################################
# Advanced stock view for pros
@slash.slash(name="advanced_stonk",
             description="Show graphs and data for a certain stock",
             options=[
                 create_option(
                     name="symbol",
                     description="Ticker symbol of the stock you want to view",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="timespan",
                     description="The size of the time window",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="minute",
                             value="minute",
                         ),
                         create_choice(
                             name="hour",
                             value="hour"
                         ),
                         create_choice(
                             name="day",
                             value="day"
                         ),
                         create_choice(
                             name="week",
                             value="week"
                         ),
                         create_choice(
                             name="month",
                             value="month"
                         ),
                         create_choice(
                             name="quarter",
                             value="quarter"
                         ),
                         create_choice(
                             name="year",
                             value="year"
                         )
                     ]
                 ),
                 create_option(
                     name="multiplier",
                     description="The size of the timespan multiplier",
                     option_type=4,
                     required=False
                 ),
                 create_option(
                     name="start",
                     description="YYYY-MM-DD",
                     option_type=3,
                     required=False
                 ),
                 create_option(
                     name="end",
                     description="YYYY-MM-DD",
                     option_type=3,
                     required=False
                 )
             ])
async def _advanced_stonk(ctx, symbol: str, timespan: str = 'minute', multiplier: int = 30, start: str = ((dt.datetime.now() - dt.timedelta(days=7)).strftime("%Y-%m-%d")), end: str = dt.datetime.now().strftime("%Y-%m-%d")):
    symbol = symbol.upper()
    data = polygon.agg_df(symbol, timespan, str(multiplier), start, end, POLYGON_KEY)
    close = round(data['Close'][-1], 2)
    info = polygon.info(symbol, POLYGON_KEY)
    graphs.gen_graph(data)
    file = discord.File('plot.png', filename='plot.png')
    await ctx.send(file=file, embed=await embeds.simple_stonk(client, info, close))


# Generic stock view (easy to use)
@slash.slash(name="stonk",
             description="simple stonk info",
             options=[
                 create_option(
                     name="symbol",
                     description="Ticker symbol of the stock you want to view",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="period",
                     description="Time duration for price graph",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="day",
                             value="day"
                         ),
                         create_choice(
                             name="week",
                             value="week"
                         ),
                         create_choice(
                             name="month",
                             value="month"
                         ),
                         create_choice(
                             name="3month",
                             value="3month"
                         ),
                         create_choice(
                             name="year",
                             value="year"
                         ),
                         create_choice(
                             name="5year",
                             value="5year"
                         )
                     ]
                 ),
                 create_option(
                     name="detailed_view",
                     description="Display detailed stats on your symbol",
                     option_type=5,
                     required=False,
                 )
             ])
async def _stonk(ctx, symbol: str, period: str = "day", detailed_view: bool = False):
    symbol = symbol.upper()
    timespan, multiplier, start, subtitle = "", "", "", ""
    if period == "day":
        timespan = "minute"
        multiplier = "10"
        subtitle = "Today"
        start = dt.datetime.now().strftime("%Y-%m-%d")
    if period == "week":
        timespan = "hour"
        multiplier = "1"
        subtitle = "Past Week"
        start = (dt.datetime.now() - dt.timedelta(days=7)).strftime("%Y-%m-%d")
    if period == "month":
        timespan = "hour"
        multiplier = "12"
        subtitle = "Past Month"
        start = (dt.datetime.now() - dt.timedelta(days=30)).strftime("%Y-%m-%d")
    if period == "3month":
        timespan = "day"
        multiplier = "1"
        subtitle = "Past 3 Months"
        start = (dt.datetime.now() - dt.timedelta(days=90)).strftime("%Y-%m-%d")
    if period == "year":
        timespan = "week"
        multiplier = "1"
        subtitle = "Past Year"
        start = (dt.datetime.now() - dt.timedelta(days=365)).strftime("%Y-%m-%d")
    if period == "5year":
        timespan = "month"
        multiplier = "1"
        subtitle = "Past 5 Years"
        start = (dt.datetime.now() - dt.timedelta(days=1825)).strftime("%Y-%m-%d")
    data = polygon.agg_df(symbol, timespan, str(multiplier), start, dt.datetime.now().strftime("%Y-%m-%d"), POLYGON_KEY)
    previous = round(data['Open'][0], 2)
    now = round(data['Close'][-1], 2)
    graphs.gen_graph(data)
    file = discord.File('plot.png', filename='plot.png')
    if detailed_view:
        await ctx.send(file=file, embed=await embeds.advanced_stonk_info(client, symbol, now, previous, subtitle))
    else:
        await ctx.send(file=file, embed=await embeds.simple_stonk(client, symbol, now, previous, subtitle))


########################################################################################################################
#                                                      Bot Init                                                        #
########################################################################################################################
# Init call to discord API (Nothing below this)
client.run(DISCORD_KEY)
