from discord.ext import commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):
        await ctx.send("🎫 (Mock) Ticket aangemaakt! Support zal je helpen.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
