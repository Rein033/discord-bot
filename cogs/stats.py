import discord
from discord.ext import commands
import json
import os

STATS_FILE = "data/stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def save_stats(data):
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats = load_stats()

    def add_message(self, guild_id, user_id):
        gid = str(guild_id)
        uid = str(user_id)
        if gid not in self.stats:
            self.stats[gid] = {}
        if uid not in self.stats[gid]:
            self.stats[gid][uid] = 0
        self.stats[gid][uid] += 1
        save_stats(self.stats)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        self.add_message(message.guild.id, message.author.id)

    @commands.command()
    async def serverstats(self, ctx):
        guild = ctx.guild
        total_members = guild.member_count
        online_members = sum(1 for m in guild.members if m.status != discord.Status.offline)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)

        embed = discord.Embed(title=f"📊 Stats voor {guild.name}", color=discord.Color.purple())
        embed.add_field(name="Leden", value=total_members)
        embed.add_field(name="Online", value=online_members)
        embed.add_field(name="Tekstkanalen", value=text_channels)
        embed.add_field(name="Voicekanalen", value=voice_channels)
        await ctx.send(embed=embed)

    @commands.command()
    async def userstats(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        gid = str(ctx.guild.id)
        uid = str(member.id)
        messages = self.stats.get(gid, {}).get(uid, 0)
        await ctx.send(f"📈 {member.display_name} heeft **{messages}** berichten gestuurd!")

    @commands.command()
    async def topactive(self, ctx):
        gid = str(ctx.guild.id)
        if gid not in self.stats:
            return await ctx.send("Geen data beschikbaar.")
        sorted_users = sorted(self.stats[gid].items(), key=lambda x: x[1], reverse=True)[:10]
        embed = discord.Embed(title="🏆 Top 10 Actiefste Gebruikers", color=discord.Color.gold())
        for i, (uid, count) in enumerate(sorted_users, start=1):
            user = ctx.guild.get_member(int(uid))
            name = user.display_name if user else "Onbekend"
            embed.add_field(name=f"{i}. {name}", value=f"{count} berichten", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
