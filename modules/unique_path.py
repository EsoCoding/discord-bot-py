import random
import string
import os

from modules.logger import Logger


# Define a class called UniquePath
class UniquePath:
    # Define the __init__ method which is called when a new object is created
    def __init__(self):
        # Create an instance variable called vowels and assign it the string "aeiou"
        self.vowels = "aeiou"
        # Create an instance variable called consonants and assign it the string of all lowercase letters
        # excluding the vowels
        self.consonants = "".join(set(string.ascii_lowercase) - set(self.vowels))

    # This method generates a random word of a specified length using a combination of consonants and vowels.
    # It takes two parameters: ctx - the context object, and length - the length of the word to be generated.
    async def generate(self, ctx, length=10):
        # Initialize an empty string to store the generated word.
        word = ""

        # Iterate through the range of the specified length.
        for i in range(length):
            # Check if the current index is even.
            if i % 2 == 0:
                # If the index is even, add a random consonant to the word.
                word += random.choice(self.consonants)
            else:
                # If the index is odd, add a random vowel to the word.
                word += random.choice(self.vowels)

        # Check if the generated word is None.
        if word is None:
            # If the word is None, return False.
            return False
        else:
            # If the word is not None, construct the unique path by concatenating the temporary folder path
            # with the generated word and assign it to the 'unique_path' attribute of the context object.
            ctx.unique_path = (
                str(os.getenv("DISCORD_BOT_TEMP_FOLDER")) + "/" + str(word)
            )

            # Return True to indicate that the word generation was successful.
            return True
        
    async def delete(self, ctx):
        try:
            # Log the action of deleting the temp folder along with the unique path
            Logger.info(f"Deleting temp folder: {ctx.unique_path}")

            # Use the operating system command "rm -rf" to recursively delete the folder specified by the unique path
            os.system(f"rm -rf {ctx.unique_path}")

            # Return True to indicate that the deletion was successful
            return True
        except Exception as e:
            # Log the error message if an exception occurs during the deletion process
            Logger.error(f"Error: {str(e)}")

            # Raise a new exception with the same error message
            raise Exception(f"Error: {str(e)}")
