import discord
from discord.ext import commands

from bot.config import EMBED_COLOR, IMAGE_URL, SERVER_NAME, SHOWCASE_CARD_URL, SHOWCASE_MEMBER_ID
from bot.views.welcome import WelcomeView


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Welcome to Our Server!",
            description=(
                "We're glad to have you here! 🎉\n\n"
                "Click one of the buttons below to get started "
                "or learn more about our community."
            ),
            color=EMBED_COLOR,
        )
        member = ctx.guild.get_member(SHOWCASE_MEMBER_ID)
        embed.set_author(name=SERVER_NAME, icon_url=IMAGE_URL if IMAGE_URL.startswith("http") else None)
        embed.set_thumbnail(url=IMAGE_URL if IMAGE_URL.startswith("http") else None)
        embed.set_footer(text="Enjoy your stay!")
        if member is not None:
            embed.add_field(
                name=f"{member.display_name}'s Info",
                value=f"{member.mention}'s   [Card]({SHOWCASE_CARD_URL})",
            )
        await ctx.send(embed=embed, view=WelcomeView())


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
