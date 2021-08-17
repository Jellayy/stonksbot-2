import discord


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
    embed.set_footer(text="StonksBotDos", icon_url=client.user.avatar_url)
    embed.add_field(name="\u200B", value="*Based on your monitored stocks*")

    return embed


async def stonk_view(client, info):
    embed = discord.Embed(
        color=discord.Color.blue(),
        title=info['name'],
        description=info['description']
    )
    embed.set_author(name=info['symbol'], icon_url=info['logo'])
    embed.add_field(name="\u200B", value=f"Location: {info['hq_state']}, {info['hq_country']}")
    embed.set_footer(text="StonksBotDos", icon_url=client.user.avatar_url)
    embed.set_image(url="attachment://plot.png")

    return embed
