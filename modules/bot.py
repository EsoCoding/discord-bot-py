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
<<<<<<< HEAD
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
=======
        super().__init__(intents=Intents.all())
        self.commands = commands.Bot(command_prefix=os.environ.get("DISCORD_BOT_PREFIX"), intents=Intents.all())
        self.validation = Validation()
        self.unique_path = UniquePath()
        self.downloader = Downloader()
        self.zipfile = ZipFile()
        self.uploader = Uploader()

    def start(self):
            
        @self.commands.command(name="download", help="Download a file from a URL")
        async def download(ctx, url: str):
            # validate the url
            if await self.validation.validate(ctx, url):
                ctx.send(f"{ctx.author.mention} processing request, i'll send you a message when your haul has arrived!")
                # generate a path with a random folder name
                await self.unique_path.generate(ctx)
                # download the files
                await self.downloader.download(ctx)
                # zip the files
                await self.zipfile.zipfile(ctx)
                # upload the files
                if await self.uploader.upload_file(ctx):
                    
                    user = await self.commands.fetch_user(int(ctx.author.id))
                    await self.message_user(ctx, user, f"Here is your haul {ctx.go_file_link}")
                    
                    Logger.info(f"sended message to {ctx.author.name} with download link: {ctx.go_file_link}")
                    
                # delete the temp folder
                if await self.unique_path.delete(ctx):
                    Logger.info("Deleted temp folder")

            elif await self.validation.validate(ctx, url) == False:
                # Log the error
                Logger.error("Invalid URL")
                raise commands.errors.CommandInvokeError("Invalid URL")
            elif await url == None:
                #log error
                Logger.error("Missing required argument")
                raise commands.errors.MissingRequiredArgument("Missing required argument")
            
        @self.commands.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.errors.MissingRequiredArgument):
                await ctx.send("Missing required argument")
            elif isinstance(error, commands.errors.CommandInvokeError):
                await ctx.send("Invalid URL")
            else:
                await ctx.send(error)
        

        self.commands.run(os.environ.get("DISCORD_BOT_TOKEN"))

    async def message_user(self, context, user: discord.User, message):
        await user.send(message)


    async def on_ready(self):
        Logger.info(f"You are now logged in as: {self.commands.user}")

>>>>>>> parent of 90d0351 (feat: Add new feature)
