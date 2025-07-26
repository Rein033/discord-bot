from discord.ext import commands

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx):
        await ctx.send(f"{ctx.author.mention}, jouw huidige level is: 1 (mock)")

async def setup(bot):
    await bot.add_cog(Leveling(bot))
