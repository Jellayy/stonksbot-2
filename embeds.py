import discord
import requests
import VERY_SECRET_LAUNCH_CODES


async def outage_alert(client):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Outage Notice",
        description="I'm putting my computer in a box. Stonksbot will be down. Suck my nuts."
    )
    embed.set_footer(text="StonksBotDos", icon_url=client.user.avatar_url)

    return embed


async def stonk_syntax_error(client):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Invalid Syntax",
        description="**Usage:** gib stonk [TICKER] (TIMEFRAME) (MULTIPLIER) (START: YYYY-MM-DD) (END: YYYY-MM-DD)"
    )
    embed.set_footer(text="StonksBotDos", icon_url=client.user.avatar_url)
    embed.add_field(name="\u200B", value="*querying outside of market hours can throw this exception as well*")

    return embed


async def stonk_data_error(client):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Data Error",
        description="This error is maybe really bad. See if API is giving realtime data."
    )
    embed.set_footer(text="StonksBotDos", icon_url=client.user.avatar_url)
    embed.add_field(name="\u200B", value="*ben might have to pay for api lol*")

    return embed


async def stonk_view(client, ticker):
    r = requests.get(f'https://api.polygon.io/v1/meta/symbols/{ticker}/company?&apiKey={VERY_SECRET_LAUNCH_CODES.HYDROGEN_LAUNCH_CODE()}')
    data = r.json()
    embed = discord.Embed(
        color=discord.Color.blue(),
        title=data['name'],
        description=data['description']
    )
    embed.set_author(name=ticker, icon_url=data['logo'])
    embed.add_field(name="\u200B", value=f"Location: {data['hq_state']}, {data['hq_country']}")
    embed.set_image(url="attachment://plot.png")
    embed.set_footer(text="StonksBotDos", icon_url=client.user.avatar_url)
    try:
        r = requests.get(
            f'https://api.polygon.io/v1/meta/symbols/{ticker}/news?perpage=50&page=1&apiKey={VERY_SECRET_LAUNCH_CODES.HYDROGEN_LAUNCH_CODE()}')
        news = r.json()[0]
        embed.add_field(name="News:", value=f"**{news['title']}**\n{news['summary']}\n*{news['url']}*", inline=False)
    except IndexError:
        embed.add_field(name="News:", value="*No articles found*")

    return embed
