import discord


async def stonk_syntax_error(client):
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Invalid Syntax",
        description="**Usage:** gib stonk [TICKER] [(opt)START(YYYY-M-D)] [(opt)END(YYYY-M-D)]"
    )
    embed.set_footer(text="StonksBotDos", icon_url=client.user.avatar_url)

    return embed
