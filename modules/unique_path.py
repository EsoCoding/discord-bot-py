import random
import string
import sys
import os

from modules.logger import Logger


class UniquePath:
    def __init__(self):
        self.vowels = "aeiou"
        self.consonants = "".join(set(string.ascii_lowercase) - set(self.vowels))

    async def generate(self, ctx, length=10):
        word = ""
        for i in range(length):
            if i % 2 == 0:
                word += random.choice(self.consonants)
            else:
                word += random.choice(self.vowels)

        if word is None:
            return False
        else:
            ctx.unique_path = (
                str(os.getenv("DISCORD_BOT_TEMP_FOLDER")) + "/" + str(word)
            )

            return True
