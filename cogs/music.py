import discord
from discord.ext import commands
import asyncio
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []  # Queue van nummers
        self.playing = False

    # ✅ Command: join voice channel
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"✅ Verbonden met {channel}")
        else:
            await ctx.send("❌ Je zit niet in een voice kanaal!")

    # ✅ Command: leave voice channel
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("❌ Bot is uit voice kanaal gegaan.")
        else:
            await ctx.send("❌ Ik ben niet in een voice kanaal!")

    # ✅ Command: play muziek
    @commands.command()
    async def play(self, ctx, *, url: str):
        if not ctx.voice_client:
            await self.join(ctx)

        self.queue.append(url)
        await ctx.send(f"🎵 Toegevoegd aan queue: {url}")

        if not self.playing:
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if self.queue:
            url = self.queue.pop(0)
            self.playing = True

            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']

            source = await discord.FFmpegOpusAudio.from_probe(audio_url, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'})
            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))

            await ctx.send(f"▶️ Nu aan het spelen: {url}")
        else:
            self.playing = False

    # ✅ Command: skip nummer
    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Nummer geskipt!")
        else:
            await ctx.send("❌ Er wordt niks afgespeeld.")

    # ✅ Command: pause
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Muziek gepauzeerd.")
        else:
            await ctx.send("❌ Geen muziek om te pauzeren.")

    # ✅ Command: resume
    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Muziek hervat.")
        else:
            await ctx.send("❌ Niks om te hervatten.")

    # ✅ Command: stop
    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            self.queue.clear()
            ctx.voice_client.stop()
            await ctx.send("⏹️ Muziek gestopt en queue geleegd.")
        else:
            await ctx.send("❌ Ik speel geen muziek af.")

async def setup(bot):
    await bot.add_cog(Music(bot))
