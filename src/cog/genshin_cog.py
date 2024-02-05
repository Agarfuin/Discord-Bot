import os
from discord.ext import commands, tasks
from datetime import datetime, timedelta

class genshin_cog(commands.Cog):
    def __init__(self, bot, scraper):
        self.bot = bot
        self.scraper = scraper
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.daily_check.start()
        
    @commands.command(name="get_codes")
    async def get_codes(self, ctx):
        await ctx.send(f"**Most recent codes:**\n\n{self.scraper.print_codes()}\n{ctx.author.mention}")
        
    @commands.command(name="update_codes")
    async def update_codes(self, ctx):
        if(self.scraper.update_codes()):
            await ctx.send(f"{self.scraper.print_codes()}\n{ctx.author.mention}")
        else:
            await ctx.send(f"**No new codes for now master...**\n\n{ctx.author.mention}")
            
    @tasks.loop(seconds=60)
    async def daily_check(self):
        now = datetime.now()
        target_time = datetime(now.year, now.month, now.day, 12, 0, 0)
        
        if now >= target_time:
            target_time += timedelta(days=1)
        
        delta_target = target_time - now
        delta_target_secs = delta_target.total_seconds()
        
        if 0 <= delta_target_secs <= 60:
            channel = self.bot.get_channel(int(os.getenv("CHANNEL_ID")))
            if channel and self.scraper.update_codes():
                user = self.bot.get_user(int(os.getenv("AGARFUIN_USER_ID")))
                await channel.send(f"**My master, your slave found some new codes:**\n\n{self.scraper.print_codes()}\n{user.mention}")
            else:
                await channel.send("**Couldn't find any new codes today master...**")
          
          
          
          
