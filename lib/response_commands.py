from discord.ext import commands
from replit import db
from concurrent.futures import ThreadPoolExecutor
from lib.bot import bot
import asyncio
import os
import openai

bot = bot()
openai.api_key = os.environ['OPENAI_KEY']


class ResponseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def evaluate(self, ctx):
        try:
            if 'debate' in db.keys():
                debate_system_prompt = """You are an AI assistant who will perform as a formal debate judge,
                analyzing the arguments, rebuttals, cross-examinations, logical fallacies, etc of the discussion. Use the users names as recorded. Provide a summary of their opinions, along with a breakdown of the reasons why. Provide approximate scoring if possible. Do not introduce yourself, just commence immediately with your analysis"""
                conversation = [{"role": "system", "content": debate_system_prompt}]
                # get history
                conversation.extend([dict(entry) for entry in db["debate"]])
                # append newest message
                debate_prompt = "Provide a very brief analysis of the discussion as if you were performing as a formal debate judge. Present a summary of each users position, with estimated points, major strengths and weaknesses with examples and classifications. Try to keep each users section to a single paragraph or so"
                conversation.append({"role": "user", "content": debate_prompt})
                # get newest response
                loop = asyncio.get_event_loop()
                with ThreadPoolExecutor() as executor:
                    response = await loop.run_in_executor(
                        executor, fetch_openai_response_sync, conversation
                    )

                reply = response.choices[0]["message"]["content"].strip()
                await ctx.channel.send(reply)
            else:
                await ctx.channel.send("No debate record found")
        except Exception:
            await ctx.channel.send("Error creating debate summary")
