from discord.ext import commands
from ledger import get_user_stats

def setup(bot):
    @bot.command(name="stats")
    async def stats(ctx, user: commands.MemberConverter = None):
        user = user or ctx.author
        stats = get_user_stats(user.id)

        message = (
            f"📊 Stats for {user.mention}:\n"
            f"• Total Bets: {stats['total_bets']}\n"
            f"• Wins: {stats['wins']} ({stats['win_rate']}%)\n"
            f"• Amount Won: ${stats['amount_won']:.2f}\n"
            f"• Amount Lost: ${stats['amount_lost']:.2f}\n"
            f"• Net Gain: ${stats['net_gain']:.2f}"
        )

        await ctx.send(message)