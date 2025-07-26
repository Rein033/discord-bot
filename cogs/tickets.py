import discord
from discord.ext import commands
import json
import os

TICKET_FILE = "data/tickets.json"

def load_tickets():
    if not os.path.exists(TICKET_FILE):
        return {}
    with open(TICKET_FILE, "r") as f:
        return json.load(f)

def save_tickets(data):
    with open(TICKET_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tickets = load_tickets()

    def get_ticket_count(self, guild_id):
        return self.tickets.get(str(guild_id), {}).get("count", 0)

    def increment_ticket(self, guild_id):
        gid = str(guild_id)
        if gid not in self.tickets:
            self.tickets[gid] = {"count": 0}
        self.tickets[gid]["count"] += 1
        save_tickets(self.tickets)
        return self.tickets[gid]["count"]

    @commands.command()
    async def ticket(self, ctx):
        """Maak een nieuw support ticket"""
        ticket_num = self.increment_ticket(ctx.guild.id)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        category = discord.utils.get(ctx.guild.categories, name="Tickets")
        if not category:
            category = await ctx.guild.create_category("Tickets")
        ticket_channel = await ctx.guild.create_text_channel(f"ticket-{ticket_num}", overwrites=overwrites, category=category)
        await ticket_channel.send(f"🎫 Hallo {ctx.author.mention}, een stafflid helpt je zo. Gebruik `!close` om dit ticket te sluiten.")
        await ctx.send(f"✅ Ticket aangemaakt: {ticket_channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def close(self, ctx):
        """Sluit het huidige ticket"""
        if ctx.channel.category and ctx.channel.category.name == "Tickets":
            await ctx.send("❌ Dit ticket wordt gesloten in 5 seconden...")
            await ctx.channel.delete(delay=5)
        else:
            await ctx.send("❌ Dit commando kan alleen in een ticketkanaal gebruikt worden.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
