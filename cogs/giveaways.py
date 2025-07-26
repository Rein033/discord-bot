from discord.ext import commands

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def giveaway(self, ctx):
        await ctx.send("🎉 (Mock) Giveaway gestart! Gebruik react om deel te nemen.")

async def setup(bot):
    await bot.add_cog(Giveaways(bot))
