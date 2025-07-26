from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"👋 Hallo {ctx.author.mention}!")

async def setup(bot):
    await bot.add_cog(Basic(bot))
