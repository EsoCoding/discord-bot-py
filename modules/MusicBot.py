# Import the os and discord libraries
import os
# Import the discord library
import discord
from discord import Intents
from discord.ext import commands
# Import the logger, URLValidator, UniquePath, 
# Downloader, ZipFile, and Uploader classes
from modules.logger import Logger
from modules.validate import Validation
from modules.unique_path import UniquePath
from modules.downloader import Downloader
from modules.zipfile import ZipFile
from modules.uploader import Uploader

# This class represents the MusicBot

class MusicBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        
        # Create a Discord bot client with a specified command prefix and all available intents
        client = commands.Bot(
            command_prefix=os.getenv("DISCORD_BOT_PREFIX"), intents=Intents.all()
        )

        # Create an instance of the UniquePath class
        self.unique_path = UniquePath()

        # Create an instance of the URLValidator class
        self.validation = Validation()

        # Create an instance of the Downloader class
        self.downloader = Downloader()

        # Create an instance of the ZipFile class
        self.zipfile = ZipFile()

        # Create an instance of the Uploader class
        self.uploader = Uploader()
        
        client.command(name="download", aliases=["dl"], help="Download files from a URL.")
        # Decorate the 'dl' method as a command that can be invoked through the Discord bot
        
    
        # Decorate the 'on_ready' method as an event handler for when the bot is ready

        @client.event
        async def on_ready():
            """
            A function that is called when the bot is ready.

            Parameters:
                self (class): The instance of the class.
            
            Returns:
                None
            """
            Logger.info(f"Bot is now logged in as {self.client.user}")
            # set status of the bot to online
            await self.change_presence(
                status=discord.Status.online, activity=None
            )

    async def download(self, ctx, arg):
        """
        Cooldown decorator for the `dl` command.
        
        Parameters:
            ctx (commands.Context): The context of the command.
            arg (str): The argument passed to the command.
        
        Returns:
            None
        
        Description:
            This function is a command that downloads files given a URL. It first validates the URL using the `validate` method from the `validation` object. If the URL is valid, it generates a unique path with a random folder name using the `generate` method from the `unique_path` object. Then, it downloads the files using the `download` method from the `downloader` object. After that, it zips the files using the `zipfile` method from the `zipfile` object. If the zipping is successful, it uploads the files using the `upload_file` method from the `uploader` object. If the upload is successful, it sends a message to the specified channel using the `send` method from the `channel` object. Finally, it deletes the temporary folder using the `delete` method from the `unique_path` object.
        
        Note:
            - This function assumes that the `validation`, `unique_path`, `downloader`, `zipfile`, `uploader`, and `channel` objects have been properly initialized.
            - The `ctx.go_file_link` variable is used in the message sent to the channel.
        """
        # validate the url
        if await self.validation.validate(ctx, arg):
            # generate a path with a random folder name
            await self.unique_path.generate(ctx)
            # download the files
            await self.downloader.download(ctx)
            # zip the files
            await self.zipfile.zipfile(ctx)
            # upload the files
            if await self.uploader.upload_file(ctx):
                
                # send a message to the channel
                channel_id = int(os.environ.get("DISCORD_BOT_CHANNEL_ID"))
                # get the channel object
                channel = self.client.get_channel(channel_id)
                # check channel exists and send message
                if channel is None:
                    Logger.error(f"Error: Could not find channel with ID {channel_id}")
                else:
                    await channel.send(f"{ctx.author.mention} your present is ready: {ctx.go_file_link}")     
                    Logger.info(f"sended message to channel to {ctx.author.mention} with upload link: {ctx.go_file_link}")
            # delete the temp folder
            if await self.unique_path.delete(ctx):
                Logger.info("Deleted temp folder")

        else:
            # Log the error
            Logger.error("Invalid URL")
            await ctx.send("Invalid URL")

        # Event handler for when the bot receives a command error  # event decorator/wrapper
        @self.client.event
        async def on_command_error(ctx, error):
            """
            Handles errors that occur during command execution.

            Parameters:
                ctx (commands.Context): The context of the command.
                error (commands.CommandError): The error that occurred.

            Returns:
                None
            
            Raises:
                None
            """
            
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f"This command is on cooldown, please retry in {error.retry_after:.2f}s.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"Missing required argument: {error.param.name}")
            elif isinstance(error, commands.BadArgument):   
                await ctx.send(f"Bad argument: {error}")
            elif isinstance(error, commands.MemberNotFound):   
                await ctx.send(f"Could not find member by given string")
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send(f"Missing permissions: {error}")
            elif isinstance(error, commands.BotMissingPermissions):
                await ctx.send(f"Bot missing permissions: {error}")
            elif isinstance(error, commands.CommandNotFound):
                await ctx.send(f"Command not found: {error}")
            elif isinstance(error, commands.CheckFailure):
                await ctx.send(f"Check failure: {error}")
            elif isinstance(error, commands.CommandInvokeError):
                Logger.info(f"Command error: {error}")
                await ctx.send(f"Command error: {error}")
            else:
                await ctx.send(f"Unknown error: {error}")
        
        async def on_message(self, message):
            """
            Asynchronously handles an incoming message.

            Args:
                self (object): The instance of the class.
                message (object): The message object received.

            Returns:
                None
            """
            # Process the message
            await self.client.process_commands(message)

            # Event handler for when the bot receives a command error  # event decorator/wrapper
        @self.client.event
        async def on_message(self, message):
            await self.client.process_commands(message)

            for mention in message.role_mentions:
                print(mention.name)
                