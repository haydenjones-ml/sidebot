import discord

from discord.ext import commands

def setup(bot):
    @bot.command(name="sidebet")
    async def bet(ctx, bettor1: discord.Member, bettor2: discord.Member, amount: int):
        return