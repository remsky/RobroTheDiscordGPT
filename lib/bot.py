import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)