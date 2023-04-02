from discord.ext import commands
from replit import db
from concurrent.futures import ThreadPoolExecutor
from lib.utils import summarize_link, extract_url, remove_read_link
from lib.bot import bot
import asyncio
import os
import openai
from lib.bot import bot
bot = bot()

openai.api_key = os.environ['OPENAI_KEY']


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.command()
    async def ping(self, ctx):
        """ Pings the bot"""
        await ctx.send("Robro is here")
    
          
    # @commands.command(name='listen', aliases=['l'])
    # async def _listen(self, ctx, *, message):
    #     """ Replies to the user message """
    #     # reply = bot.reply(message)
    #     await ctx.send(reply)
  