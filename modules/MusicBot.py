# Import the os and discord libraries
import os
import discord

# Import discord class and Intents class
# from the discord library
from discord import Intents
from discord.ext import commands

# import custom modules
from modules.Fetcher import Fetcher
from modules.Logger import Logger


# This class represents the MusicBot
class MusicBot:
    # This is the constructor of the MusicBot class
    def __init__(self):
        # Create a Discord bot with the specified command prefix and intents
        self.client = commands.Bot(
            command_prefix=os.getenv("DISCORD_BOT_PREFIX"), intents=Intents.all()
        )

        # Event handler for when the bot is ready
        @self.client.event
        async def on_ready():
            # Log that the bot is logged in and print it to the console
            Logger.info(f"Bot is now logged in as {self.client.user}")
            # set status of the bot to online
            await self.client.change_presence(
                status=discord.Status.online, activity=None
            )

        # Event handler for when the bot receives a message
        @self.client.event
        async def on_message(message):
            # Log the message and the author
            Logger.info(f"Received message {message.content} from {message.author}")
            # Process the message
            await self.client.process_commands(message)

        # Event handler for when the bot receives a command error
        @self.client.event  # event decorator/wrapper
        async def on_command_error(ctx, error):
            # Log the error and send an error message
            Logger.error(f"Error: {str(error)}")
            await ctx.send(f"Error: {str(error)}")

        # Command handler for the "dt" command
        @self.client.command()
        async def dt(ctx, arg):
            try:
                # Log the received command and the author
                Logger.info(f"Received command {ctx.command} from {ctx.author}")

                # Fetch the filename using the Fetcher module
                fatch_url = Fetcher()
                fetched_url = fatch_url.create_upload_file_from_stream_rip(
                    arg, ctx.author
                )

                # return error or link to file on gofile.io
                return ctx.send(
                    ctx.message.author.mention + " for your addiction: " + fetched_url
                )

            except Exception as e:
                # Log and send an error message
                Logger.error(f"Error: {str(e)}")
                await ctx.send(f"Error: {str(e)}")
