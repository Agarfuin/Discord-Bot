import os
import time
from discord.ext import commands

class general_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(int(os.getenv("CHANNEL_ID")))
        await channel.send("**Greetings master, waiting for your orders...**")
        
    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send("**Testing, attention please...**")
        
    @commands.command(name="delete")
    async def delete_messages(self, ctx, amount: int):
        if ctx.message.author.guild_permissions.manage_messages:
            deleted_messages = await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Deleted {len(deleted_messages) - 1} message(s).\n\n{ctx.author.mention}")
            time.sleep(5)
            await ctx.channel.purge(limit=1)
        else:
            await ctx.send("You don't have the permission to manage messages.")
            
            
            

