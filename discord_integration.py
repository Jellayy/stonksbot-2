import discord
from discord.ext import commands, tasks
import datetime as dt
import embeds
import api
import VERY_SECRET_LAUNCH_CODES
import yfinance as yf


# CONFIGURATION
ALERT_CHANNEL = 'investing'


client = commands.Bot(command_prefix='gib ')


# Print log when logged in
@client.event
async def on_ready():
    print(f'[{dt.datetime.now().time()}] Logged in as {client.user}')
    gme_alert.start()
    update_status.start()


# Updates status with current GME Price
@tasks.loop(minutes=1)
async def update_status():
    if dt.time(1) <= dt.datetime.now().time() <= dt.time(17):
        try:
            gme = yf.Ticker('GME')
            price = round(gme.history(period='1d', interval='1m', prepost='True', actions='False').iloc[-1]['Close'], 2)
            await client.change_presence(activity=discord.Activity(name=f"GME: ${price}", type=3))
            print(f"[{dt.datetime.now().time()}] Task: Update Status: GME: ${price}")
        except RuntimeError:
            await client.change_presence(activity=discord.Activity(name="yfinance down", type=3))


# Detects large moving 5min trends in GME and sends alerts to server if so
@tasks.loop(minutes=5)
async def gme_alert():
    if dt.time(1) <= dt.datetime.now().time() <= dt.time(17):
        gme = yf.Ticker('GME')
        previous = gme.history(period='1d', interval='1m', prepost='True', actions='False').iloc[-6]['Close']
        now = gme.history(period='1d', interval='1m', prepost='True', actions='False').iloc[-1]['Close']
        percent_change = round(((now - previous) / previous) * 100, 2)
        five_min_dif = round(now - previous, 2)
        if percent_change >= 3:
            for guild in client.guilds:
                for channel in guild.channels:
                    if str(channel) == ALERT_CHANNEL:
                        await channel.send(f"GME **+${five_min_dif}** | **+{percent_change}%** last 5 min \n <@226927637971337216> <@114712079683944450> <@178310541691977728> <@265710358151430144>")
                        print(f"[{dt.datetime.now().time()}] Task: GME Alert: 3% 5min Upward Trend Triggered")
        elif percent_change <= -3:
            for guild in client.guilds:
                for channel in guild.channels:
                    if str(channel) == ALERT_CHANNEL:
                        await channel.send(f"GME **${five_min_dif}** | **{percent_change}%** last 5 min \n <@226927637971337216> <@114712079683944450> <@178310541691977728> <@265710358151430144>")
                        print(f"[{dt.datetime.now().time()}] Task: GME Alert: 3% 5min Downward Trend Triggered")
        else:
            print(f"[{dt.datetime.now().time()}] Task: GME Alert: No Trend Detected")


# This looks terrible because making the bot use code blocks is disgusting, I will never use this again
@client.command()
async def ping(ctx):
    await ctx.send(f"""
```
Latency: {round(client.latency*1000, 3)}ms
```
""")


# This command does literally everything rn bc testing, will split up later maybe
@client.command()
async def stonk(ctx, stock=None, timespan='minute', multiplier=int(5), start=((dt.datetime.today() - dt.timedelta(days=5)).strftime("%Y-%m-%d")), end=(dt.datetime.today()).strftime("%Y-%m-%d")):
    if stock is None:
        await ctx.channel.send(embed=await embeds.stonk_syntax_error(client))
    else:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%d")
            end = dt.datetime.strptime(end, "%Y-%m-%d")
            api.gen_graph(stock, timespan, multiplier, start, end)
            file = discord.File('plot.png', filename="plot.png")
            await ctx.channel.send(file=file, embed=await embeds.stonk_view(client, stock.upper()))
        except KeyError:
            await ctx.channel.send(embed=await embeds.stonk_syntax_error(client))
        except ValueError:
            await ctx.channel.send(embed=await embeds.stonk_data_error(client))

client.run(VERY_SECRET_LAUNCH_CODES.PLUTONIUM_LAUNCH_CODE())
