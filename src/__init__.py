import discord
import os, asyncio
from dotenv import load_dotenv
from discord.ext import commands

from util.Scraper import Scraper
from cog.general_cog import general_cog
from cog.genshin_cog import genshin_cog
from cog.music_cog import music_cog


load_dotenv()
scraper = Scraper(os.getenv("ADDRESS"))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    async with bot:
        await bot.add_cog(general_cog(bot))
        await bot.add_cog(genshin_cog(bot, scraper))
        await bot.add_cog(music_cog(bot))
        await bot.start(os.getenv("DISCORD_TOKEN"))
    

if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    
    