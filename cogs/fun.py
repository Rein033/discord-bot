from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong! 🏓")

    @commands.command()
    async def joke(self, ctx):
        await ctx.send("Waarom is programmeren net als magie? Omdat één verkeerde spreuk alles kan breken! 🪄")

async def setup(bot):
    await bot.add_cog(Fun(bot))
