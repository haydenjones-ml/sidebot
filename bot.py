import discord
import json
import os

from discord.ext import commands

# Load API keys as arrays, grab each "value" as its key param

def load_api_keys():
    config_path = 'token.json'
    with open(config_path, 'r') as file:
        config = json.load(file)
        return config["APP_ID"], config["DISCORD_TOKEN"], config["PUBLIC_KEY"]
    
app_id, discord_token, public_key = load_api_keys()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

#INSERT COMMAND FUNCTIONALITY BELOW HERE
#TODO: CREATE BETTING COMMANDS, LEDGER COMMANDS ON PER-SERVER BASIS, STATS PAGE OPT.

from sidebet import setup as sidebet_setup
from stats import setup as stats_setup

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

sidebet_setup(bot)
stats_setup(bot)
bot.run(discord_token)
