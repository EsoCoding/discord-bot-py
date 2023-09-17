import os
import openai
import aiohttp

from flask import Flask, render_template
from flask_socketio import SocketIO

import discord
from discord.ext import commands

from modules.logger import Logger

class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.commands = commands.Bot(command_prefix=os.environ.get("DISCORD_BOT_PREFIX"), intents=discord.Intents.all())

    async def get_openai_response(self, prompt):
        api_key = os.environ.get("OPENAI_API_KEY")
        processed_input = self.handle_langchain(prompt)
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": processed_input}
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                response_json = await response.json()
                return response_json['choices'][0]['message']['content'].strip()

    def handle_langchain(self, input_text):
        return input_text.upper()

    async def on_ready(self):
        Logger.info(f"You are now logged in as: {self.user}")

    async def on_message(self, message):
        
        if message.author == self.user:
            Logger.info(f" talking to myself {message.author.name} and {self.user.name}")
            return
        else:
            Logger.info(f" talking to bot {message.author.name} and {self.user.name}")

        if not message.content.startswith('!'):
            openai_response = await self.get_openai_response(message.content)
            await message.channel.send(f'OpenAI: {openai_response}')

        
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("Command not found.")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Missing required argument.")
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send("Bad argument.")
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Could not find member by given string.")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Missing permissions.")
        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.send("Bot missing permissions.")
        else:
            await ctx.send("Something went wrong.")