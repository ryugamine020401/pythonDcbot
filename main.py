import discord
from dotenv import load_dotenv
import os

load_dotenv()



BOT_TOKEN = os.getenv("BOT_TOKEN")


class Client(discord.Client):
    async def on_ready(self):
        """
        當 bot 啟動時會做的事
        """
        print(f"{self.user} Online now!")


intents = discord.Intents.default()
intents.message_content = True

client = Client(intents = intents)
client.run(BOT_TOKEN)