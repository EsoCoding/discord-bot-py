import random
import string
import sys


class NameGenerator:
    def __init__(self):
        self.vowels = "aeiou"
        self.consonants = "".join(set(string.ascii_lowercase) - set(self.vowels))

    async def generate_word(self, ctx, length=10) -> None:
        word = ""
        for i in range(length):
            if i % 2 == 0:
                word += random.choice(self.consonants)
            else:
                word += random.choice(self.vowels)

        ctx.generated_name = word
