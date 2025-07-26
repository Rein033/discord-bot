import discord
from discord.ext import commands
import json
import os

CONFIG_FILE = "data/config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    def get_guild_config(self, guild_id):
        return self.config.get(str(guild_id), {})

    def set_guild_config(self, guild_id, key, value):
        gid = str(guild_id)
        if gid not in self.config:
            self.config[gid] = {}
        self.config[gid][key] = value
        save_config(self.config)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        """Stel het logkanaal in."""
        self.set_guild_config(ctx.guild.id, "log_channel", channel.id)
        await ctx.send(f"✅ Log kanaal ingesteld op {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setallowed(self, ctx, *channels: discord.TextChannel):
        """Stel toegestane kanalen in voor botcommando's."""
        ids = [ch.id for ch in channels]
        self.set_guild_config(ctx.guild.id, "allowed_channels", ids)
        await ctx.send(f"✅ Toegestane kanalen ingesteld: {', '.join([ch.mention for ch in channels])}")

    @commands.command()
    async def settings(self, ctx):
        """Bekijk huidige instellingen."""
        cfg = self.get_guild_config(ctx.guild.id)
        log_channel = f"<#{cfg.get('log_channel')}>" if 'log_channel' in cfg else "Niet ingesteld"
        allowed_channels = ", ".join([f"<#{c}>" for c in cfg.get('allowed_channels', [])]) or "Geen restricties"
        await ctx.send(f"**Instellingen:**\nLog kanaal: {log_channel}\nToegestane kanalen: {allowed_channels}")

async def setup(bot):
    await bot.add_cog(Config(bot))
