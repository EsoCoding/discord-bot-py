from urllib.parse import urlparse
class URLValidator():
    def __init__(self):
        pass

    async def validate(ctx, arg):
        try:
            result = urlparse(arg)
            return all([result.scheme, result.netloc]) and (result.netloc == "www.qobuz.com" or result.netloc == "www.deezer.com")
        except ValueError:
            return ctx.on_command_error("Invalid URL")
    