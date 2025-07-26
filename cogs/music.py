from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url: str):
        await ctx.send(f"🎵 (Mock) Speelt muziek van: {url}")

async def setup(bot):
    await bot.add_cog(Music(bot))
