import discord
from discord.ext import commands
import datetime as dt
import embeds
import api
import VERY_SECRET_LAUNCH_CODES

five_day_delta = dt.timedelta(days=5)

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
async def stonk(ctx, stock=None, timespan='minute', multiplier=int(5), start=((dt.datetime.today()-five_day_delta).strftime("%Y-%m-%d")), end=dt.datetime.today().strftime("%Y-%m-%d")):
    if stock is None:
        await ctx.channel.send(embed=await embeds.stonk_syntax_error(client))
    else:
        try:
            api.gen_graph(stock, timespan, multiplier, start, end)
            file = discord.File('plot.png', filename="plot.png")
            await ctx.channel.send(file=file, embed=await embeds.stonk_view(client, stock.upper()))
        except KeyError:
            await ctx.channel.send(embed=await embeds.stonk_syntax_error(client))

client.run(VERY_SECRET_LAUNCH_CODES.PLUTONIUM_LAUNCH_CODE())
