import discord
from discord.ext import commands, tasks
import aiohttp
import os
import json
import asyncio

CONFIG_FILE = "data/config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.twitch_check.start()
        self.youtube_check.start()
        self.twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_token = os.getenv("TWITCH_TOKEN")
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.live_status = {}  # Houdt bij wie live is

    def cog_unload(self):
        self.twitch_check.cancel()
        self.youtube_check.cancel()

    # ✅ Command: Set kanaal voor notificaties
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setnotify(self, ctx, channel: discord.TextChannel):
        gid = str(ctx.guild.id)
        if gid not in self.config:
            self.config[gid] = {}
        self.config[gid]["notify_channel"] = channel.id
        save_config(self.config)
        await ctx.send(f"✅ Notificaties worden gestuurd naar {channel.mention}")

    # ✅ Twitch check elke 60 sec
    @tasks.loop(seconds=60)
    async def twitch_check(self):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Client-ID": self.twitch_client_id,
                "Authorization": f"Bearer {self.twitch_token}"
            }
            for gid, settings in self.config.items():
                if "twitch_user" in settings:
                    user = settings["twitch_user"]
                    async with session.get(f"https://api.twitch.tv/helix/streams?user_login={user}", headers=headers) as resp:
                        data = await resp.json()
                        if data["data"]:
                            # Live
                            if user not in self.live_status or not self.live_status[user]:
                                self.live_status[user] = True
                                channel = self.bot.get_channel(settings["notify_channel"])
                                await channel.send(f"🎮 **{user} is nu LIVE op Twitch!**\nhttps://twitch.tv/{user}")
                        else:
                            self.live_status[user] = False

    # ✅ YouTube check elke 120 sec
    @tasks.loop(seconds=120)
    async def youtube_check(self):
        async with aiohttp.ClientSession() as session:
            for gid, settings in self.config.items():
                if "youtube_channel_id" in settings:
                    channel_id = settings["youtube_channel_id"]
                    async with session.get(f"https://www.googleapis.com/youtube/v3/search?channelId={channel_id}&order=date&part=snippet&type=video&maxResults=1&key={self.youtube_api_key}") as resp:
                        data = await resp.json()
                        if "items" in data and len(data["items"]) > 0:
                            video = data["items"][0]
                            video_id = video["id"]["videoId"]
                            if settings.get("last_video") != video_id:
                                settings["last_video"] = video_id
                                save_config(self.config)
                                channel = self.bot.get_channel(settings["notify_channel"])
                                await channel.send(f"📢 Nieuwe YouTube video van **{video['snippet']['channelTitle']}**:\nhttps://youtu.be/{video_id}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settwitch(self, ctx, username: str):
        gid = str(ctx.guild.id)
        if gid not in self.config:
            self.config[gid] = {}
        self.config[gid]["twitch_user"] = username
        save_config(self.config)
        await ctx.send(f"✅ Twitch gebruiker ingesteld op: {username}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setyoutube(self, ctx, channel_id: str):
        gid = str(ctx.guild.id)
        if gid not in self.config:
            self.config[gid] = {}
        self.config[gid]["youtube_channel_id"] = channel_id
        save_config(self.config)
        await ctx.send(f"✅ YouTube kanaal ingesteld op: {channel_id}")

async def setup(bot):
    await bot.add_cog(Notifications(bot))
