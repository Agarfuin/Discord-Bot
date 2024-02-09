import os
from discord.ext import commands, tasks
from datetime import datetime, timedelta

class genshin_cog(commands.Cog):
    def __init__(self, bot, scraper):
        self.bot = bot
        self.scraper = scraper
        
    def print_codes(self, codes):
        ret_str = ""
        if(codes):
            for code in codes:
                ret_str += f"[{code}](<https://genshin.hoyoverse.com/en/gift?code={code}>)\n"
            return ret_str
        return None
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.daily_check.start()
        
    @commands.command(name="get_codes")
    async def get_codes(self, ctx):
        try:
            await ctx.send(f"**Most recent codes:**\n\n{self.print_codes(self.scraper.get_codes())}\n{ctx.author.mention}")
        except Exception as e:
            print(f"{e}")
        
    @commands.command(name="update_codes")
    async def update_codes(self, ctx):
        try:
            new_codes = self.scraper.update_codes()
            if(new_codes):
                await ctx.send(f"{self.print_codes(new_codes)}\n{ctx.author.mention}")
            else:
                await ctx.send(f"**No new codes for now master...**\n\n{ctx.author.mention}")
        except Exception as e:
            print(f"{e}")
            
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
            new_codes = self.scraper.update_codes()
            if channel and new_codes:
                user = self.bot.get_user(int(os.getenv("AGARFUIN_USER_ID")))
                await channel.send(f"**My master, your slave found some new codes:**\n\n{self.print_codes(new_codes)}\n{user.mention}")
            else:
                await channel.send("**Couldn't find any new codes today master...**")




