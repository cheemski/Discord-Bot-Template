import discord
from discord.ext import commands

from bot.config import EMBED_COLOR, IMAGE_URL, SERVER_NAME
from bot.views.service_request import ServiceRequestView


class ServiceRequest(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def servicerequest(self, ctx: commands.Context):
        embed = discord.Embed(
            title=f"欢迎来到 {SERVER_NAME}! 🎉",
            description=(
                "很开心你加入我们～"
                "点击下方按钮提交服务需求，或了解更多社群资讯。"
                "希望你在这里玩得开心，找到喜欢的伙伴！"
            ),
            color=EMBED_COLOR,
        )
        embed.set_author(name=SERVER_NAME, icon_url=IMAGE_URL if IMAGE_URL.startswith("http") else None)
        embed.set_thumbnail(url=IMAGE_URL if IMAGE_URL.startswith("http") else None)
        embed.set_footer(text="Enjoy your stay!")

        await ctx.send(embed=embed, view=ServiceRequestView())


async def setup(bot: commands.Bot):
    await bot.add_cog(ServiceRequest(bot))
