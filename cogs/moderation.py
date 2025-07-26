import discord
from discord.ext import commands
import json
import os

CONFIG_FILE = "data/config.json"
WARNS_FILE = "data/warnings.json"

# Helper functions
def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_json(CONFIG_FILE)
        self.warnings = load_json(WARNS_FILE)

    def get_log_channel(self, guild_id):
        guild_id = str(guild_id)
        if guild_id in self.config and "log_channel" in self.config[guild_id]:
            return self.config[guild_id]["log_channel"]
        return None

    async def log_action(self, guild, message):
        log_channel_id = self.get_log_channel(guild.id)
        if log_channel_id:
            channel = guild.get_channel(log_channel_id)
            if channel:
                await channel.send(f"📢 **Moderation Log:** {message}")

    # ✅ Kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Geen reden opgegeven"):
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member} is gekickt. Reden: {reason}")
        await self.log_action(ctx.guild, f"{ctx.author} heeft {member} gekickt. Reden: {reason}")

    # ✅ Ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Geen reden opgegeven"):
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member} is verbannen. Reden: {reason}")
        await self.log_action(ctx.guild, f"{ctx.author} heeft {member} verbannen. Reden: {reason}")

    # ✅ Unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        name, discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == name and user.discriminator == discriminator:
                await ctx.guild.unban(user)
                await ctx.send(f"✅ {user} is ge-unbanned!")
                await self.log_action(ctx.guild, f"{ctx.author} heeft {user} ge-unbanned.")
                return
        await ctx.send("❌ Gebruiker niet gevonden in de banlijst.")

    # ✅ Mute (rol-gebaseerd)
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False)
        await member.add_roles(role)
        await ctx.send(f"✅ {member} is gemuted.")
        await self.log_action(ctx.guild, f"{ctx.author} heeft {member} gemuted.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"✅ {member} is ge-unmuted.")
            await self.log_action(ctx.guild, f"{ctx.author} heeft {member} ge-unmuted.")
        else:
            await ctx.send("❌ Deze gebruiker is niet gemuted.")

    # ✅ Warn command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Geen reden opgegeven"):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.warnings:
            self.warnings[guild_id] = {}
        user_id = str(member.id)
        if user_id not in self.warnings[guild_id]:
            self.warnings[guild_id][user_id] = []
        self.warnings[guild_id][user_id].append(reason)
        save_json(WARNS_FILE, self.warnings)
        await ctx.send(f"⚠️ {member.mention} heeft een waarschuwing gekregen. Reden: {reason}")
        await self.log_action(ctx.guild, f"{ctx.author} heeft {member} gewaarschuwd: {reason}")

    # ✅ Clear messages
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"✅ {amount} berichten verwijderd.", delete_after=5)
        await self.log_action(ctx.guild, f"{ctx.author} heeft {amount} berichten verwijderd in {ctx.channel.mention}.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
