import discord
from discord.ext import commands

class CommandCog(commands.Cog):
    """
    放監聽事件的Cog Class
    """
    def __init__(self, bot):
        self.bot_check = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @commands.command(aliases=["乒"])
    async def PING(self, ctx):
        await ctx.send(f"PONG! {ctx.author.name}")

    @commands.command()
    async def embed(self, ctx):
        embed_message = discord.Embed(
            title = "烏薩奇",
            description = "嗚拉呀哈，呀哈嗚拉。\n嗚呀咿哈!!!!!!!\n咿呀~~~咕嚕嚕嚕嚕嚕嚕嚕嚕嚕嚕嚕嚕。",
            color = discord.Color.green()
        )
        embed_message.set_image(url = ctx.author.avatar)
        embed_message.add_field(name="うさぎ", value="ウラヤハ－ヤハウラ", inline=True)
        embed_message.set_thumbnail(url = ctx.guild.icon)
        embed_message.set_footer(text="兔子", icon_url="https://w7.pngwing.com/pngs/602/130/png-transparent-letter-lowercase-o-red-letters-and-numbers-icon.png")

        await ctx.send(embed=embed_message)

async def setup(bot):
    await bot.add_cog(CommandCog(bot = bot))