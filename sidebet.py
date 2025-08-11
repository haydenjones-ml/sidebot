import discord
from discord import app_commands
from ledger import add_sidebet, settle, get_all_bets, get_my_bets

def setup(bot, guild=None):
    @bot.tree.command(name="bet", description="Create a new sidebet", guild=guild)
    @app_commands.describe(bettor1="First bettor", bettor2="Second bettor", amount="Amount in USD")
    async def bet(interaction: discord.Interaction, bettor1: discord.Member, bettor2: discord.Member, amount: int):
        bet_id = add_sidebet(interaction.guild.id, bettor1.id, bettor2.id, amount)
        await interaction.response.send_message(f"Bet {bet_id} created: {bettor1.mention} vs {bettor2.mention} for ${amount}")

    @bot.tree.command(name="settle_bet", description="Settle a bet by ID and winner", guild=guild)
    @app_commands.describe(bet_id="ID of the bet to settle", winner="Winner of the bet")
    async def settle_bet(interaction: discord.Interaction, bet_id: int, winner: discord.Member):
        settle(bet_id, winner.id)
        await interaction.response.send_message(f"Bet {bet_id} settled! Congrats to {winner.mention}")

    @bot.tree.command(name="ledger", description="Show recent bets in this server", guild=guild)
    async def ledger(interaction: discord.Interaction):
        bets = get_all_bets(interaction.guild.id)
        if not bets:
            await interaction.response.send_message("The ledger is empty! Place your bets.")
            return

        bets_arr = []
        for bet in bets[-5:]:
            status = "Open" if bet["Open"] else "Settled"
            winner_str = f", Winner: <@{bet['winner']}>" if bet["winner"] else ""
            line = f"#{bet['bet_id']}: <@{bet['bettor_1_id']}> vs <@{bet['bettor_2_id']}> for ${bet['amount']} – Status: {status}{winner_str}"
            bets_arr.append(line)

        await interaction.response.send_message("\n".join(bets_arr))

    @bot.tree.command(name="view_my_bets", description="Shows YOUR most recent bets (in this server)", guild=guild)
    async def view_my_bets(interaction: discord.Interaction):
        user_id = interaction.user.id
        server_id = interaction.guild.id
        bets = get_my_bets(server_id=server_id, user_id=user_id)
        if not bets:
            await interaction.response.send_message("You currently have no bets! Place bets to see bet data.")
            return
        

        response_lines = []
        for bet in bets[-5:]:
            status = "Open" if bet["Open"] else "Settled"
            winner_str = f", Winner: <@{bet['winner']}>" if bet["winner"] else ""
            line = f"#{bet['bet_id']}: <@{bet['bettor_1_id']}> vs <@{bet['bettor_2_id']}> for ${bet['amount']} – Status: {status}{winner_str}"
            response_lines.append(line)

        await interaction.response.send_message(f"\n".join(response_lines))

