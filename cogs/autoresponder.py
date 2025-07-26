from discord.ext import commands

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addresponse(self, ctx, trigger: str, *, response: str):
        await ctx.send(f"✅ Auto-response toegevoegd: '{trigger}' → '{response}' (mock)")

async def setup(bot):
    await bot.add_cog(AutoResponder(bot))
