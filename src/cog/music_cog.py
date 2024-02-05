import discord
import youtube_dl as ydl
from discord.ext import commands
import asyncio

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'extractor_args': {'youtube': {'skip': 'dash_manifest,manifest,uploader_id'}},
        }

        self.vc = None
        self.ydl = ydl.YoutubeDL(self.YDL_OPTIONS)
            
    @commands.command(name="play", aliases=["p"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        info = self.ydl.extract_info(f'ytsearch:{query}', download=False)
        url2 = info['entries'][0]['formats'][0]['url']
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        voice_channel.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e))

        await ctx.send(f'Now playing: {info["entries"][0]["title"]}')
                    
    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            
    @commands.command(name = "resume", help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)
            
    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"#{i+1} -" + self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(f"```queue:\n{retval}```")
        else:
            await ctx.send("```No music in queue```")

    @commands.command(name="disconnect", aliases=["dc"], help="Kick the bot from VC")
    async def dc(self, ctx):
        if self.vc != None:
            self.vc.stop()
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        await self.vc.disconnect()
    
    @commands.command(name="remove", aliases=["rm"], help="Removes last song added to queue")
    async def re(self, ctx):
        self.music_queue.pop()
        await ctx.send("```last song removed```")
        
        
        
        
    