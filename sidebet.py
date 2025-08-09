import discord

from discord.ext import commands
from ledger import add_sidebet, settle, get_all_bets, get_open_bets

def setup(bot):
    @bot.command(name="bet")
    async def bet(ctx, bettor1: discord.Member, bettor2: discord.Member, amount: int):
        bet_id = add_sidebet(ctx.guild.id, bettor1.id, bettor2.id, amount)
        await ctx.send(f"Bet {bet_id} created: {bettor1.mention} vs {bettor2.mention} for {amount}")
    
    @bot.command(name="settle_bet")
    async def settle_bet(ctx, bet_id: int, winner: discord.Member):
        settle(bet_id, winner.id)
        await ctx.send(f"Bed {bet_id} settled! Congrats to {winner.mention}")

    @bot.command(name="ledger")
    async def ledger_cmd(ctx):
        bets = get_all_bets()
        if not bets:
            await ctx.send("The ledger is empty! Place your bets.")
            return
        
        bets_arr = []
        for bet in bets[-5:]: #Should show last bets
            line = f"#{bet['bet_id']}: <@{bet['bettor_1_id']}> vs <@{bet['bettor_2_id']}> for ${bet['amount']} – Status: {bet['status']}"
            if bet['Open']:
                line += f", Winner: <@{bet['winner']}>"
            bets_arr.append(line)

        await ctx.send("\n".join(bets_arr))

        