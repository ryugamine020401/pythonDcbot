import discord
from discord.ext import commands 
from discord import app_commands
import random, aiohttp, aiosqlite, os
from dotenv import load_dotenv
load_dotenv()

DB = os.getenv("DB_NAME")

class SlashCommandCog(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is oline!")

    @app_commands.command(name="divination", description="擲茭")
    async def divination(self, interation :discord.Interaction, question :str):
        result = random.randint(1, 4)

        if result == 1:
            result = "笑杯"
        elif result == 2:
            result = "陰杯"
        else:
            result = "聖杯"

        embed = discord.Embed(
             title="擲茭結果",
             color=discord.Color.red() if result=="陰杯" else discord.Color.green(),
             description=f"關於你的提問 {question} 神明最終決定"
        )
        embed.add_field(name=result, value=result, inline=True)
        embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4WAKkMvinyKXrooHFBCS6b7CHjC74GRaVbw&s")
        result = "可以" if result == "聖杯" else "不行"
        await interation.response.send_message(f"{interation.user.mention} 問: {question}", embed=embed)

    @app_commands.command(name="register", description="輸入自己的username來註冊")
    async def register(self, interaction: discord.Interaction, username: str):
        """
        發送 POST 請求來註冊 DC 用戶
        """
        payload = {"username": username}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post("https://35.229.237.202/api/UsersManager/dc_register_user/", json=payload) as response:
                    if response.status == 200:
                        async with aiosqlite.connect(DB) as db:
                            async with db.execute(
                                "SELECT 1 FROM userdata WHERE dc_user_uid = ?", (interaction.user.id,)
                            ) as cursor:
                                existing_user = await cursor.fetchone()

                            if existing_user:
                                await interaction.response.send_message(f"⚠️ 你已經註冊過了！", ephemeral=True)
                                return

                            await db.execute(
                                "INSERT INTO userdata (dc_user_uid, username) VALUES (?, ?)",
                                (interaction.user.id, username)
                            )
                            await db.commit()

                        await interaction.response.send_message(f"✅ 註冊成功！已經將你的 Discord 綁訂到 **{username}** ！", ephemeral=True)

                    elif response.status == 404:
                        await interaction.response.send_message(f"⚠️ 註冊失敗，沒有這個使用者", ephemeral=True)

                    else:
                        await interaction.response.send_message(f"⚠️ 註冊失敗，狀態碼：{response.status}", ephemeral=True)

            except Exception as e:
                await interaction.response.send_message(f"❌ API 連線失敗：{e}", ephemeral=True)

    @app_commands.command(name="unregister", description="輸入 username 來解除綁定")
    async def unregister(self, interaction: discord.Interaction, username: str):
        """
        確認 username 與 Discord ID 是否匹配，並從資料庫移除
        """
        async with aiosqlite.connect(DB) as db:
            async with db.execute(
                "SELECT username FROM userdata WHERE dc_user_uid = ?", (interaction.user.id,)
            ) as cursor:
                result = await cursor.fetchone()

            if not result:
                await interaction.response.send_message(f"⚠️ 找不到 username {username} 的綁定記錄！", ephemeral=True)
                return
            stored_username = result[0]

            if stored_username != username:
                await interaction.response.send_message(f"❌ 綁定的 username 和輸入的不匹配 ！", ephemeral=True)
                return

            await db.execute("DELETE FROM userdata WHERE dc_user_uid = ?", (interaction.user.id,))
            await db.commit()

        await interaction.response.send_message(f"✅ `{username}` 綁定解除成功！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashCommandCog(bot = bot))