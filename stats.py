import discord
from discord import app_commands
from ledger import get_user_stats

def setup(bot, guild=None):

    @bot.tree.command(name="stats", description="Get betting stats for a user")
    @app_commands.describe(user="User to get stats for (default: yourself)")
    async def stats(interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        stats = get_user_stats(user.id)

        message = (
            f"📊 Stats for {user.mention}:\n"
            f"• Total Bets: {stats['total_bets']}\n"
            f"• Wins: {stats['wins']} ({stats['win_rate']}%)\n"
            f"• Amount Won: ${stats['amount_won']:.2f}\n"
            f"• Amount Lost: ${stats['amount_lost']:.2f}\n"
            f"• Net Gain: ${stats['net_gain']:.2f}"
        )
        await interaction.response.send_message(message)