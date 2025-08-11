import discord
import json
from discord.ext import commands

DEV_GUILD_ID = 1403656083314184292  # Your test server

def load_api_keys():
    with open('token_bank.json', 'r') as file:
        config = json.load(file)
        return config["APP_ID"], config["DISCORD_TOKEN"], config["PUBLIC_KEY"]

app_id, discord_token, public_key = load_api_keys()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

MY_GUILD = discord.Object(id=DEV_GUILD_ID)  # dev guild object

# Import and setup commands
from sidebet import setup as sidebet_setup
from stats import setup as stats_setup

sidebet_setup(bot, MY_GUILD)
stats_setup(bot, MY_GUILD)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=MY_GUILD)
    print(f"Synced commands to dev guild {DEV_GUILD_ID}")
    print(f"Loaded guild commands: {[cmd.name for cmd in bot.tree.get_commands(guild=MY_GUILD)]}")


bot.run(discord_token)