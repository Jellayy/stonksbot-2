import discord
from discord.ext import commands, tasks
import datetime as dt
from configparser import ConfigParser


# Read config.ini
parser = ConfigParser()
parser.read('config.ini')
DISCORD_KEY = parser.get('settings', 'discord.py api key')
PREFIX = parser.get('settings', 'command prefix') + " "
MONITORED_STOCKS = parser.get('settings', 'monitored stocks').split(",")


client = commands.Bot(command_prefix=PREFIX)


# Run on login
@client.event
async def on_ready():
    print(f'[{dt.datetime.now().time().strftime("%H:%M:%S")}] Logged in as {client.user}')

# Init call to discord API (Nothing below this)
client.run(DISCORD_KEY)
