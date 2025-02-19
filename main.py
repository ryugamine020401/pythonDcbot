import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

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

# @bot.event
# async def on_message(msg):
#     """
#     當 bot 收到聊天室的訊息 會和 command 牴觸
#     """
#     if msg.author == bot.user:
#         return
#     if msg.content.startswith('hello'):
#         await msg.channel.send(f"hi {msg.author}")

@bot.event
async def on_message_delete(msg):
    """
    刪除訊息的事件
    """
    if msg.author.bot:
        return

    channel = bot.get_channel(msg.channel.id)
    await channel.send((f" 刪除了 {msg.author.mention} 在 {msg.channel.name} 說的 : 『{msg.content}』"))

@bot.event
async def on_member_join(member):
    """
    伺服器成員加入的事件
    """
    welcome_channel_id = WELCOME_CHANNEL_ID
    channel = bot.get_channel(welcome_channel_id)
    
    try:
        message = f"(●´ω｀●)ゞ 恭請 {member.global_name} 駕到。"
        await member.send(message)
    except Exception as e:
        print(f"main.py 49, \n{e}")

    await channel.send(f"Welcome {member.global_name} join {member.guild} at {member.joined_at}.\n{member.avatar}")

@bot.event
async def on_member_update(before, after):
    """
    成員編輯伺服器的個人資訊時會做的事情
    """
    if before.display_name != after.display_name:
        message = f"抓到偷改名喔 (｡A｡) {before.display_name}"
    else:
        message = f"偷改 (｡A｡)"
    try:
        await after.send(message)
        print(f"成功DM {after.name}")
    except discord.Forbidden:
        print(f"{after.name} 禁用了DM")


@bot.command(aliases=["hi", "yo"])
async def hello(ctx):
    await ctx.send("hi")



bot.run(token=BOT_TOKEN)