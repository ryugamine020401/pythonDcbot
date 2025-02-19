import discord
from discord.ext import commands
from dotenv import load_dotenv
import os, asyncio

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    """
    當 bot 啟動時會做的事
    """
    print(f"{bot.user} Online now!")


async def Load():
    for filename in (os.listdir("./Cogs")):
        # print(filename)
        if filename.endswith(".py"):
            await bot.load_extension(f"Cogs.{filename[:-3]}")

async def main():
    async with bot:
        await Load()
        await bot.start(token = BOT_TOKEN)


asyncio.run(main = main())