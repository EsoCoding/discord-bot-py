from urllib.parse import urlparse
from modules.logger import Logger

class URLValidator():
    def __init__(self):
        pass

    async def validate(self, ctx, arg):
        """
        Validate the given URL and store it in the 'url' attribute of the 'ctx' object.

        Parameters:
            ctx (object): The context object that stores information about the command.
            arg (str): The URL to be validated.

        Returns:
            bool: True if the URL is valid and the 'netloc' component is either "www.qobuz.com" or "www.deezer.com". False otherwise.
        """
        try:
            result = urlparse(arg)  # Parse the given URL and retrieve its components
            ctx.url = arg  # Store the given URL in the 'url' attribute of the 'ctx' object
            Logger.info("Proccesing your gift!")  # Log an informational message
            # Check if both 'scheme' and 'netloc' components of the parsed URL are not empty,
            # and if the 'netloc' component is either "www.qobuz.com" or "www.deezer.com"
            return all([result.scheme, result.netloc]) and (result.netloc == "www.qobuz.com" or result.netloc == "www.deezer.com")        
        except ValueError:
            return ctx.on_command_error("Invalid URL")
    