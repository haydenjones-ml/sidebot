import discord

from discord.ext import commands
from ledger import add_sidebet, settle, get_all_bets, get_open_bets

def setup(bot):
    @bot.command(name="bet")
    async def bet(ctx, bettor1: discord.Member, bettor2: discord.Member, amount: int):
        bet_id = add_sidebet(ctx.guild.id, bettor1.id, bettor2.id, amount)
        await ctx.send(f"Bet {bet_id} created: {bettor1.mention} vs {bettor2.mention} for {amount}")