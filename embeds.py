import discord


async def stonk_syntax_error(client):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Invalid Syntax",
        description="**Usage:** gib stonk [TICKER] (TIMEFRAME) (MULTIPLIER) (START: YYYY-MM-DD) (END: YYYY-MM-DD)"
    )
    embed.set_footer(text="StonksBotDos", icon_url=client.user.avatar_url)
    embed.add_field(name="\u200B", value="*querying outside of market hours can throw this exception as well*")

    return embed
