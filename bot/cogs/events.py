import discord
from discord.ext import commands

from bot.config import (
    EMBED_COLOR,
    LOBBY_CHANNEL_URL,
    SELF_ORDER_CHANNEL_URL,
    SERVER_NAME,
    WELCOME_CHANNEL_ID,
)


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)

        embed = discord.Embed(
            title=f"💝 欢迎您来到✨ {SERVER_NAME} ✨ !",
            color=EMBED_COLOR,
        )
        embed.description = (
            f"🎮 主营游戏\nValorant ・ CS2 ・ Apex ・ League of Legends・Steam\n\n\n"
            f"💼 服务类型\n"
            f"🌸 娱乐陪玩｜轻松聊天 & 情绪价值\n"
            f"🔥 技术陪玩｜稳定上分 & 指导\n\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👩‍🚀可自助下单/到接待大厅联系客服/私信客服！\n"
            f"✨希望板板在 {SERVER_NAME} 能找到属于您的快乐！\n"
            f"➤[⁠「🌸接待大厅」]({LOBBY_CHANNEL_URL})\n"
            f"➤[📠-自助下单]({SELF_ORDER_CHANNEL_URL})"
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        if channel:
            await channel.send(
                f"💝 欢迎您来到✨ {SERVER_NAME} ✨ !, {member.mention}!",
                embed=embed,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
