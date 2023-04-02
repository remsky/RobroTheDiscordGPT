from discord.ext import commands
from replit import db
from concurrent.futures import ThreadPoolExecutor
from lib.utils import summarize_link, extract_url, remove_read_link
from lib.bot import bot
import asyncio
import os
import openai


openai.api_key = os.environ['OPENAI_KEY']

class RecordingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startcontext(self, ctx):
        channel_id = ctx.channel.id
        bot.recording[channel_id] = True
        await ctx.send("GPT has quickened (responses are stored as short-term memory)")

    @commands.command()
    async def startdebate(self, ctx):
        bot.recording["debate"] = True
        await ctx.send("GPT has adjusted its focus to the debate")

    @commands.command()
    async def enddebate(self, ctx):
        del db['debate']
        bot.recording["debate"] = False
        await ctx.send("GPT has tired of your mortal concerns")

    @commands.command()
    async def extendcontext(self, ctx):
        bot.recording["extended"] = True
        await ctx.send("Extended context is now active with 30 total messages")

    @commands.command()
    async def standardcontext(self, ctx):
        bot.recording["extended"] = False
        await ctx.send("Context is returned to 7 total messages")

    @commands.command()
    async def endcontext(self, ctx):
        channel_id = ctx.channel.id
        bot.recording[channel_id] = False
        await ctx.send("GPT has slowed (responses are no longer stored as short-term memory)")

