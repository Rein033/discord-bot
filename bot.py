import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Laad environment variables (.env)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")

# Intents (nodig voor berichten en members)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Maak bot instance
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ✅ Event: bot is online
@bot.event
async def on_ready():
    print(f"✅ Bot is online als {bot.user}")

# ✅ Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Je hebt geen permissie voor dit commando.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("⚠️ Onbekend commando. Typ !help voor opties.")
    else:
        await ctx.send(f"⚠️ Er ging iets mis: {error}")

# ✅ Auto-load alle cogs in de map /cogs/
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")

# ✅ Main loop
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
