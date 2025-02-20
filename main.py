import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os, asyncio, random, aiosqlite
from itertools import cycle
import aiohttp


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DB = os.getenv("DB_NAME")
DEV_ID = int(os.getenv("DEV_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)
bot_status = cycle(["尖尖挖嘎乃", "嗚啦", "チャルメラ"])

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


async def init_db():
    """
    初始化 SQLite 數據庫
    """
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dc_user_uid INTEGER NOT NULL UNIQUE,
                username TEXT NOT NULL
            )
        """)
        await db.commit()

@bot.event
async def on_ready():
    """
    當 bot 啟動時會做的事
    """
    print(f"{bot.user} Online now!")

    change_bot_status.start()
    send_webhook_report.start()
    check_limit.start()
    try:
        synced_command = await bot.tree.sync()
        print(f"synced {len(synced_command)} comand.")
    except Exception as e:
        print(f"main.py Error 64 {e}")

    await init_db()

@bot.tree.command(name="helloworld", description="Hello World!!!!!")
async def hi(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} hello!!", ephemeral=True)

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


@tasks.loop(minutes=1440)
async def check_limit():
    """
    從 SQLite 資料庫中獲取所有註冊的 dc_user_uid，並私訊該用戶
    """
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT dc_user_uid, username FROM userdata") as cursor:
            users = await cursor.fetchall()  # 取得所有用戶 ID
    all_username = []
    for username in users:
        all_username.append(username[1])

    payload = {
        "username" : all_username
    }
    dict_user_id = {dc_username : dc_user_id for dc_user_id, dc_username in users}
    async with aiohttp.ClientSession() as session:
            try:
                async with session.post("http://35.229.237.202:38777/api/ProductsManager/dc_get_product/", json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        pass
                    else:
                        pass

            except Exception as e:
                print(f"❌ API 連線失敗：{e}")

    for i in data['data'].items():
        # print(i[0]) # username
        # print(i[1]) # 過期、快過期的商品
        # print(dict_user_id[i[0]])   # userid
        if len(i[1]['Expired']) != 0 or len(i[1]['ExpiredSoon']) != 0:
            embed = discord.Embed(
                title="有效期限提醒"
            )
            
            for product in i[1]['Expired']:
                # print(f"過期的產品 : {product}")
                embed.add_field(
                    name="❌ 已過期",
                    value=product,
                    inline=True
                )
            for product in i[1]['ExpiredSoon']:
                # print(f"過期的產品 : {product}")
                embed.add_field(
                    name="⚠️ 快過期",
                    value=product,
                    inline=True
                )
            
            try:
                user = await bot.fetch_user(dict_user_id[i[0]])
                if user:
                    await user.send(embed=embed)
            except Exception as e:
                print(f"main.py 189 error {e}")


def get_cogs():
    """
    取得 Cogs 資料夾內的所有 Python 檔案 (去掉 `.py`)
    """
    return [f[:-3] for f in os.listdir("Cogs") if f.endswith(".py") and not f.startswith("__")]


@bot.tree.command(name="load", description="可以載入指定的 Cog")
@app_commands.choices(
    extension=[app_commands.Choice(name=cog, value=cog) for cog in get_cogs()]
)
async def load(interaction: discord.Interaction, extension: str):
    if interaction.user.id == DEV_ID:
        print(interaction.user.id)
        try:
            await bot.load_extension(f"Cogs.{extension}")
            await interaction.response.send_message(f"成功載入 Cog {extension}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"載入 Cog {extension}失敗, Because {e}", ephemeral=True)
    else:
        await interaction.response.send_message(f"權限不足.", ephemeral=True)


@bot.tree.command(name="reload", description="可以重新載入指定的 Cog")
@app_commands.choices(
    extension=[app_commands.Choice(name=cog, value=cog) for cog in get_cogs()]
)
async def reload(interaction: discord.Interaction, extension: str):
    if interaction.user.id == DEV_ID:
        try:
            await bot.reload_extension(f"Cogs.{extension}")
            await interaction.response.send_message(f"Reload {extension} done.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"fail to Reload {extension}. Because {e}", ephemeral=True)
            print(f"重新載入 Cogs 失敗 main.py 175 {e}")
    else:
        await interaction.response.send_message(f"權限不足.", ephemeral=True)


@bot.tree.command(name="unload", description="可以移除指定的 Cog")
@app_commands.choices(
    extension=[app_commands.Choice(name=cog, value=cog) for cog in get_cogs()]
)
async def unload(interaction: discord.Interaction, extension: str):
    if interaction.user.id == DEV_ID:
        try:
            await bot.unload_extension(f"Cogs.{extension}")
            await interaction.response.send_message(f"成功移除 Cog {extension}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"移除 Cog {extension} 失敗. Because {e}", ephemeral=True)
    else:
        await interaction.response.send_message(f"權限不足.", ephemeral=True)



asyncio.run(main = main())