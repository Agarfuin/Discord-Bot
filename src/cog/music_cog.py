import discord
import yt_dlp
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        
        self.YDL_OPTIONS = {
            'format': 'bestaudio',
            'title': True,
            'cookiefile': '/cookies/cookies.txt',
        }
        self.FFMPEG_OPTIONS = {
            'options': '-vn',
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        }
        
        self.ydl = yt_dlp.YoutubeDL(self.YDL_OPTIONS)
        self.voice_client = None
        
    async def play_next(self, ctx):
        if not self.is_paused:
            if not self.music_queue:
                self.is_playing = False
                return
            self.is_playing = True
            song_info, voice_channel = self.music_queue.pop(0)
            
            if self.voice_client == None or not self.voice_client.is_connected():
                self.voice_client = await voice_channel.connect()
                
            url = song_info.get('url')
            await ctx.send(f"**Now playing: {song_info.get('title')}**")
            self.voice_client.play(discord.FFmpegPCMAudio(url, executable= "ffmpeg", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
         
    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *args):
        try:
            query = " ".join(args)
            if not ctx.author.voice or not ctx.author.voice.channel:
                await ctx.send("**Master, please connect to a voice channel...**")
                return

            voice_channel = ctx.author.voice.channel
            song_info = self.ydl.extract_info(query, download=False)
            self.music_queue.append([song_info, voice_channel])
            
            if self.is_playing or self.is_paused:
                await ctx.send(f"**{song_info.get('title')} added to the queue.**")
                return
                
            await self.play_next(ctx)
        except Exception as e:
            print(e)
                    
    @commands.command(name="pause", aliases=["stop"])
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.voice_client.pause()
            
    @commands.command(name = "resume", aliases=["continue"])
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.voice_client.resume()

    @commands.command(name="skip", aliases=["s"])
    async def skip(self, ctx):
        if self.voice_client is not None:
            self.voice_client.stop()
            await self.play_next(ctx)
            
    @commands.command(name="queue", aliases=["q"])
    async def queue(self, ctx):
        ret_str = ""
        for i in range(0, len(self.music_queue)):
            ret_str += f"#{i+1} - {self.music_queue[i][0].get('title')}\n"

        if ret_str != "":
            await ctx.send(f"**Queue:**\n```{ret_str}```")
        else:
            await ctx.send("**No music in queue master...**")

    @commands.command(name="disconnect", aliases=["dc"])
    async def dc(self, ctx):
        if self.voice_client != None:
            await self.voice_client.disconnect()
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        await self.voice_client.disconnect()
    
    @commands.command(name="remove", aliases=["rm"])
    async def remove(self, ctx, index: int):
        if(index > len(self.music_queue)):
            await ctx.send("**Sorry master, index is out of range...**")
            return
        song_info, _ = self.music_queue.pop(index-1)
        await ctx.send(f"**As you wish, {song_info.get('title')} removed from the queue...**")
        
        
        
        
    