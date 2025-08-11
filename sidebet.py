import discord
from discord import app_commands
from ledger import add_sidebet, settle, get_all_bets, get_my_bets

PAGE_SIZE = 5

def setup(bot, guild=None):
    #CREATED CLASS FOR LEDGER / (EVENTUAL) ALL BET PAGINATION
    class BetPagination(discord.ui.View):
        def __init__(self, bets, user_id):
            super().__init__(timeout=300) # Need timeout for pagination requests (after 5 min, stop accepting interaction)
            self.bets = sorted(bets, key=lambda b: b["bet_id"], reverse=True)
            self.current_page = 0
            self.user_id = user_id

        def format_page(self):
            start = self.current_page * PAGE_SIZE
            end = start + PAGE_SIZE
            bet_page = self.bets[start:end]

            if not bet_page:
                return "Nothing to see here."
            
            bets_arr = []
            for bet in bet_page:
                status = "Open" if bet["Open"] else "Settled"
                winner_str = f", Winner: <@{bet['winner']}>" if bet["winner"] else ""
                line = f"#{bet['bet_id']}: <@{bet['bettor_1_id']}> vs <@{bet['bettor_2_id']}> for ${bet['amount']} – Status: {status}{winner_str}"
                bets_arr.append(line)

            return "\n".join(bets_arr)
        
        # Restrict access of pagination to command user only
        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("You cannot interact with these! (Command user only)")
                return False
            return True
        
        @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
        async def previous(self, interaction: discord.Interaction, button: discord.ui.button):
            if self.current_page > 0:
                self.current_page -= 1
                await interaction.response.edit_message(content=self.format_page(), view=self)
            else:
                await interaction.response.defer()
        
        @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
        async def next(self, interaction: discord.Interaction, button: discord.ui.button):
            if (self.current_page + 1 * PAGE_SIZE) < len(self.bets):
                self.current_page += 1
                await interaction.response.edit_message(content=self.format_page(), view=self)
            else:
                await interaction.response.defer()

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

        view = BetPagination(bets, interaction.user.id)
        await interaction.response.send_message(content=view.format_page(), view=view)

    @bot.tree.command(name="view_my_bets", description="Shows YOUR most recent bets (in this server)", guild=guild)
    async def view_my_bets(interaction: discord.Interaction):
        user_id = interaction.user.id
        server_id = interaction.guild.id
        bets = get_my_bets(server_id=server_id, user_id=user_id)
        if not bets:
            await interaction.response.send_message("You currently have no bets! Place bets to see bet data.")
            return
        
        view = BetPagination(bets, interaction.user.id)
        await interaction.response.send_message(content=view.format_page(), view=view)