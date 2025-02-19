import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))


class ListenerCog(commands.Cog):
    """
    放監聽事件的Cog Class
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is oline!")
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
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
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        伺服器成員加入的事件
        """
        welcome_channel_id = WELCOME_CHANNEL_ID
        channel = self.bot.get_channel(welcome_channel_id)
        try:
            message = f"(●´ω｀●)ゞ 恭請 {member.global_name} 駕到。"
            await member.send(message)
        except Exception as e:
            print(f"main.py 49, \n{e}")

        await channel.send(f"Welcome {member.global_name} join {member.guild} at {member.joined_at}.\n{member.avatar}")
    
    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        """
        刪除訊息的事件
        """
        if msg.author.bot:
            return

        channel = self.bot.get_channel(msg.channel.id)
        await channel.send((f" 刪除了 {msg.author.mention} 在 {msg.channel.name} 說的 : 『{msg.content}』"))
    # @commands.Cog.listener()
    # async def on_message(msg):
    #     """
    #     當 bot 收到聊天室的訊息 會和 command 牴觸
    #     """
    #     if msg.author == bot.user:
    #         return
    #     if msg.content.startswith('hello'):
    #         await msg.channel.send(f"hi {msg.author}")


async def setup(bot):
    await bot.add_cog(ListenerCog(bot = bot))