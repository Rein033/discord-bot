import discord
from discord.ext import commands
import json
import os
import random

LEVEL_FILE = "data/leveling.json"

# Helpers
def load_data():
    if not os.path.exists(LEVEL_FILE):
        return {}
    with open(LEVEL_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(LEVEL_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = load_data()

    def get_user_data(self, guild_id, user_id):
        guild_id = str(guild_id)
        user_id = str(user_id)
        if guild_id not in self.levels:
            self.levels[guild_id] = {}
        if user_id not in self.levels[guild_id]:
            self.levels[guild_id][user_id] = {"xp": 0, "level": 1}
        return self.levels[guild_id][user_id]

    def add_xp(self, guild_id, user_id, amount):
        user_data = self.get_user_data(guild_id, user_id)
        user_data["xp"] += amount
        xp_needed = user_data["level"] * 100
        leveled_up = False
        while user_data["xp"] >= xp_needed:
            user_data["xp"] -= xp_needed
            user_data["level"] += 1
            xp_needed = user_data["level"] * 100
            leveled_up = True
        save_data(self.levels)
        return leveled_up, user_data["level"]

    # ✅ Event: XP toevoegen bij elk bericht
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        leveled_up, new_level = self.add_xp(message.guild.id, message.author.id, random.randint(10, 20))
        if leveled_up:
            await message.channel.send(f"🎉 Gefeliciteerd {message.author.mention}, je bent nu level **{new_level}**!")

    # ✅ Command: rank
    @commands.command()
    async def rank(self, ctx):
        user_data = self.get_user_data(ctx.guild.id, ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, je bent level **{user_data['level']}** met {user_data['xp']} XP.")

    # ✅ Command: leaderboard
    @commands.command()
    async def leaderboard(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.levels:
            return await ctx.send("Geen data voor deze server.")
        sorted_users = sorted(self.levels[guild_id].items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)
        top = sorted_users[:10]
        embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())
        for i, (user_id, data) in enumerate(top, start=1):
            user = ctx.guild.get_member(int(user_id))
            embed.add_field(name=f"{i}. {user.display_name if user else 'Onbekend'}", value=f"Level {data['level']} ({data['xp']} XP)", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leveling(bot))
