import discord
from discord.ext import commands 
from discord import app_commands
import random

class SlashCommandCog(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

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



async def setup(bot):
    await bot.add_cog(SlashCommandCog(bot = bot))