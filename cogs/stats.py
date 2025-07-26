from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverstats(self, ctx):
        guild = ctx.guild
        await ctx.send(f"📊 Server stats: {guild.member_count} leden, {len(guild.text_channels)} tekstkanalen")

async def setup(bot):
    await bot.add_cog(Stats(bot))
