import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os, asyncio, random
from itertools import cycle
import aiohttp


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)
bot_status = cycle(["間間挖嘎乃", "嗚啦", "チャルメラ"])

@tasks.loop(seconds=5)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

@tasks.loop(minutes=600)  # 每 60 秒執行一次
async def send_webhook_report():
    """
    透過 Webhook 發送伺服器監控報告
    """
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(WEBHOOK_URL, session=session)

        # 模擬獲取伺服器數據
        cpu_usage = random.randint(10, 90)
        memory_usage = random.randint(20, 80)
        status = "🟢 正常運行" if cpu_usage < 80 else "🔴 高負載"

        # 建立 Embed 訊息
        embed = discord.Embed(title="📊 伺服器監控報告", color=0x00ff00)
        embed.add_field(name="🖥 CPU 使用率", value=f"{cpu_usage}%", inline=True)
        embed.add_field(name="💾 記憶體使用率", value=f"{memory_usage}%", inline=True)
        embed.add_field(name="⚙ 狀態", value=status, inline=False)
        embed.set_footer(text="定期監控系統狀態")

        # 發送 Webhook 訊息
        await webhook.send(embed=embed, username="系統監控機器人")
        print("Webhook 監控報告已發送！")


@bot.event
async def on_ready():
    """
    當 bot 啟動時會做的事
    """
    print(f"{bot.user} Online now!")
    change_bot_status.start()
    send_webhook_report.start()


async def Load():
    """
    載入Cogs
    """
    for filename in (os.listdir("./Cogs")):
        # print(filename)
        if filename.endswith(".py"):
            await bot.load_extension(f"Cogs.{filename[:-3]}")

async def main():
    """
    啟動機器人
    """
    async with bot:
        await Load()
        await bot.start(token = BOT_TOKEN)


asyncio.run(main = main())