import discord
from discord.ext import commands
import json
import os

RESPONSES_FILE = "data/autoresponses.json"

def load_responses():
    if not os.path.exists(RESPONSES_FILE):
        return {}
    with open(RESPONSES_FILE, "r") as f:
        return json.load(f)

def save_responses(data):
    with open(RESPONSES_FILE, "w") as f:
        json.dump(data, f, indent=4)

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = load_responses()

    def get_guild_responses(self, guild_id):
        return self.responses.get(str(guild_id), {})

    def set_guild_response(self, guild_id, trigger, response):
        gid = str(guild_id)
        if gid not in self.responses:
            self.responses[gid] = {}
        self.responses[gid][trigger.lower()] = response
        save_responses(self.responses)

    def remove_guild_response(self, guild_id, trigger):
        gid = str(guild_id)
        if gid in self.responses and trigger.lower() in self.responses[gid]:
            del self.responses[gid][trigger.lower()]
            save_responses(self.responses)

    # ✅ Voeg response toe
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def addresponse(self, ctx, trigger: str, *, response: str):
        self.set_guild_response(ctx.guild.id, trigger, response)
        await ctx.send(f"✅ Auto-response toegevoegd: `{trigger}` → `{response}`")

    # ✅ Verwijder response
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removeresponse(self, ctx, trigger: str):
        self.remove_guild_response(ctx.guild.id, trigger)
        await ctx.send(f"✅ Auto-response verwijderd voor trigger: `{trigger}`")

    # ✅ Bekijk alle responses
    @commands.command()
    async def responses(self, ctx):
        guild_responses = self.get_guild_responses(ctx.guild.id)
        if not guild_responses:
            await ctx.send("Geen auto-responses ingesteld.")
            return
        embed = discord.Embed(title="📜 Auto-Responses", color=discord.Color.blue())
        for trigger, response in guild_responses.items():
            embed.add_field(name=trigger, value=response, inline=False)
        await ctx.send(embed=embed)

    # ✅ Luister naar berichten
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        guild_responses = self.get_guild_responses(message.guild.id)
        for trigger, response in guild_responses.items():
            if trigger.lower() in message.content.lower():
                await message.channel.send(response)
                break

async def setup(bot):
    await bot.add_cog(AutoResponder(bot))
