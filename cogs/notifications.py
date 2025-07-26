from discord.ext import commands

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def twitch(self, ctx):
        await ctx.send("📢 (Mock) Twitch notificaties zijn nog niet geconfigureerd.")

async def setup(bot):
    await bot.add_cog(Notifications(bot))
