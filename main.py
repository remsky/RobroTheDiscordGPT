import os
import re
import requests
import discord
from discord.ext import commands
import openai
from replit import db
import asyncio
from concurrent.futures import ThreadPoolExecutor
from lib.utils import summarize_link, extract_url, remove_read_link
from lib.bot import bot

from lib.recording_commands import RecordingCog
from lib.general_commands import GeneralCog
from lib.robro_commands import RobroCog


openai.api_key = os.environ['OPENAI_KEY']
discord_token = os.environ['DISCORD_BOT_SECRET']
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)
bot.add_cog(GeneralCog(bot))
bot.add_cog(RobroCog(bot))
bot.add_cog(RecordingCog(bot))
bot.add_cog()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)
bot.run(discord_token)