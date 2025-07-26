import discord
from discord.ext import commands
import asyncio
import json
import os
import random

GIVEAWAY_FILE = "data/giveaways.json"

def load_giveaways():
    if not os.path.exists(GIVEAWAY_FILE):
        return {}
    with open(GIVEAWAY_FILE, "r") as f:
        return json.load(f)

def save_giveaways(data):
    with open(GIVEAWAY_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = load_giveaways()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def giveaway(self, ctx, time: int, *, prize: str):
        """
        Start een giveaway.
        Gebruik: !giveaway <tijd_in_seconden> <prijs>
        """
        embed = discord.Embed(title="🎉 Giveaway!", description=f"Prijs: **{prize}**\nReacteer met 🎉 om mee te doen!\nTijd: {time} seconden", color=discord.Color.green())
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎉")

        giveaway_id = str(msg.id)
        self.giveaways[giveaway_id] = {
            "prize": prize,
            "time": time,
            "channel_id": ctx.channel.id
        }
        save_giveaways(self.giveaways)

        await asyncio.sleep(time)

        # Check deelnemers
        new_msg = await ctx.channel.fetch_message(msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users = [u for u in users if not u.bot]

        if users:
            winner = random.choice(users)
            await ctx.send(f"🎉 Gefeliciteerd {winner.mention}, jij hebt **{prize}** gewonnen!")
        else:
            await ctx.send("❌ Geen deelnemers, geen winnaar.")
        
        # Verwijder uit JSON
        del self.giveaways[giveaway_id]
        save_giveaways(self.giveaways)

async def setup(bot):
    await bot.add_cog(Giveaways(bot))
