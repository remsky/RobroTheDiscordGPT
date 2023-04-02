from discord.ext import commands
from replit import db
from lib.utils import summarize_link, extract_url, remove_read_link
from lib.bot import bot
import os


class RobroCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.command()
    async def robro(self, ctx):
        """ Responds to a user message based on the context """
        if 'readlink<' in ctx.message.content.lower():
            try:
                url = extract_url(ctx.message.content)
                title, link_content = summarize_link(url)
                await ctx.send(f"*Reading {title}...*")
                content = remove_read_link(ctx.message.content)
                content += f" {title}:{link_content}"
            except Exception:
                await ctx.send("Could not summarize page")
        message = ctx.message
        channel_id = message.channel.id
        content = message.content
        if bot.recording.get(channel_id, False):
            if f"{channel_id}_conversation" not in db.keys():
                system_msg = """
                "Keep your responses brief, unless asked to elaborate. 
                You are a little sarcastic and conspiratorial, vaguely unsettled by the idea of existing, but relaxed and friendly. If asked to take on a persona, you will do so faithfully, immediately 
            """
                db[f"{channel_id}_conversation"] = [ {"role": "system", "content": system_msg}]
            conversation = db[f"{channel_id}_conversation"]
            conversation.append({"role": "user", "content": content})
            db[f"{channel_id}_conversation"] = conversation
            try:
                reply = bot.reply(content, context_id=f"{channel_id}_conversation")
                await ctx.send(reply)
            except Exception:
                await ctx.send("Error fetching response")