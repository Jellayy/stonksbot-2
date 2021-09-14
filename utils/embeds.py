import discord
from configparser import ConfigParser
import yfinance as yf


########################################################################################################################
#                                                   Config Loading                                                     #
########################################################################################################################
# API config
api_parser = ConfigParser()
api_parser.read('api.ini')
POLYGON_KEY = api_parser.get('APIs', 'polygon api key')


async def daily_summary(client, biggest_moves):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Daily Summary",
        description=f'**Biggest Movers:**\n\n '
                    f'{biggest_moves[0][0]} | ${biggest_moves[0][1]} ({biggest_moves[0][2]}%)\n'
                    f'{biggest_moves[1][0]} | ${biggest_moves[1][1]} ({biggest_moves[1][2]}%)\n'
                    f'{biggest_moves[2][0]} | ${biggest_moves[2][1]} ({biggest_moves[2][2]}%)\n'
                    f'{biggest_moves[3][0]} | ${biggest_moves[3][1]} ({biggest_moves[3][2]}%)\n'
    )
    embed.set_footer(text="StonksBotDos | Powered By Polygon.io & Yahoo! Finance", icon_url=client.user.avatar_url)
    embed.add_field(name="\u200B", value="*Based on your monitored stocks*")

    return embed


async def stonk_info(client, info):
    embed = discord.Embed(
        color=discord.Color.blue(),
        title=info['name'],
        description=info['description']
    )
    embed.set_author(name=info['symbol'], icon_url=info['logo'])
    embed.add_field(name="\u200B", value=f"Location: {info['hq_state']}, {info['hq_country']}")
    embed.set_footer(text="StonksBotDos | Powered By Polygon.io & Yahoo! Finance", icon_url=client.user.avatar_url)
    embed.set_image(url="attachment://plot.png")

    return embed


async def simple_stonk(client, ticker, now, previous, subtitle):
    yfticker = yf.Ticker(ticker)
    yfinfo = yfticker.info
    delta = now - previous
    percent = round(abs((delta / now) * 100), 2)
    prefix = ""
    color = discord.Color.blue(),
    if delta > 1:
        color = discord.Color.green()
        prefix = "+"
    if delta < 1:
        color = discord.Color.red()
        prefix = "-"
    delta = round(abs(delta), 2)

    embed = discord.Embed(
        color=color,
        title=f"{yfinfo['longName']}\n${now}",
        description=f'{prefix}${delta} ({percent}%) {subtitle}'
    )
    embed.set_author(name=yfinfo['symbol'], icon_url=yfinfo['logo_url'])
    embed.set_image(url="attachment://plot.png")
    embed.set_footer(text="StonksBotDos | Powered By Polygon.io & Yahoo! Finance", icon_url=client.user.avatar_url)

    return embed


async def advanced_stonk_info(client, ticker, now, previous, subtitle):
    yfticker = yf.Ticker(ticker)
    yfinfo = yfticker.info
    delta = now - previous
    percent = round(abs((delta / now) * 100), 2)
    prefix = ""
    color = discord.Color.blue(),
    if delta > 1:
        color = discord.Color.green()
        prefix = "+"
    if delta < 1:
        color = discord.Color.red()
        prefix = "-"
    delta = round(abs(delta), 2)

    embed = discord.Embed(
        color=color,
        title=f"{yfinfo['longName']}\n${now}",
        description=f'{prefix}${delta} ({percent}%) {subtitle}'
    )
    embed.set_author(name=yfinfo['symbol'], icon_url=yfinfo['logo_url'])
    embed.set_image(url="attachment://plot.png")
    embed.add_field(name="Stats", value=f"Open: {yfinfo['regularMarketOpen']}\n"
                                        f"High: {yfinfo['regularMarketDayHigh']}\n"
                                        f"Low: {yfinfo['regularMarketDayLow']}\n"
                                        f"52 Wk High: {yfinfo['fiftyTwoWeekHigh']}\n"
                                        f"52 Wk Low: {yfinfo['fiftyTwoWeekLow']}")
    embed.add_field(name="\u200B", value=f"Volume: {yfinfo['volume24Hr']}\n"
                                         f"Avg Vol: {yfinfo['averageVolume']}\n"
                                         f"Assets: {yfinfo['totalAssets']}\n"
                                         f"PEG Ratio: {yfinfo['pegRatio']}")
    embed.set_footer(text="StonksBotDos | Powered By Polygon.io & Yahoo! Finance", icon_url=client.user.avatar_url)

    return embed
