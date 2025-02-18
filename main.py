import discord
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))

class Client(discord.Client):
    async def on_ready(self):
        """
        當 bot 啟動時會做的事
        """
        print(f"{self.user} Online now!")

    async def on_message(self ,msg):
        """
        當 bot 收到聊天室的訊息
        """
        if msg.author == self.user:
            return
        
        if msg.content.startswith('hello'):
            await msg.channel.send(f"hi {msg.author}")

    async def on_message_delete(self, msg):
        """
        刪除訊息的事件
        """
        if msg.author.bot:
            return

        channel = self.get_channel(msg.channel.id)
        await channel.send((f" 刪除了 {msg.author.mention} 在 {msg.channel.name} 說的 : 『{msg.content}』"))

    async def on_member_join(self, member):
        """
        伺服器成員加入的事件
        """
        welcome_channel_id = WELCOME_CHANNEL_ID
        channel = self.get_channel(welcome_channel_id)
        # print(dir(member))
        
        try:
            message = f"(●´ω｀●)ゞ 恭請 {member.global_name} 駕到。"
            await member.send(message)
        except Exception as e:
            print(f"main.py 49, \n{e}")

        await channel.send(f"Welcome {member.global_name} join {member.guild} at {member.joined_at}.\n{member.avatar}")
        
    async def on_member_update(self, before, after):
        """
        成員編輯
        """
        if before.display_name != after.display_name:
            message = f"抓到偷改名喔 (｡A｡) {before.display_name}"
        else:
            message = f"偷改 (｡A｡)"
        try:
            await after.send(message)
            print(f"成功發送歡迎訊息給 {after.name}")
        except discord.Forbidden:
            print(f"{after.name} 禁用了私訊，無法發送歡迎訊息。")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


client = Client(intents = intents)
client.run(BOT_TOKEN)