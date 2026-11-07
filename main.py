# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from Views.ServiceRequest import ServiceRequestView

load_dotenv()

STAFF_ROLE_ID = 1557949295775195216
WELCOME_CHANNEL_ID = 1094498216793346058
EMBED_COLOR = 0xFFB7C5
# Discord CDN attachment links expire. Use a permanent image URL instead.
IMAGE_URL = "https://cdn.discordapp.com/attachments/1533331303657898068/1559545933128274000/IMG_1602.png?ex=6acf77d5&is=6ace2655&hm=befe3a5e23e287ea2bd5a39df2a7e931b8ac21b67605d85bc76a4528ccbb0898&"

STATUS_EMOJI = {"online": "🟢", "idle": "🟡", "dnd": "🔴"}

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True


class MyBot(commands.Bot):
    async def setup_hook(self):
        # Register persistent buttons on startup
        self.add_view(WelcomeView())
        self.add_view(ServiceRequestView())


bot = MyBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    embed = discord.Embed(
            title="💝 欢迎您来到✨ 𝓔𝓔.𝓼𝓽𝓾𝓭𝓲𝓸 ✨ !",
            color=EMBED_COLOR,
        )
    embed.description = (
        f"🎮 主营游戏\nValorant ・ CS2 ・ Apex ・ League of Legends・Steam\n\n\n"
        f"💼 服务类型\n"
        f"🌸 娱乐陪玩｜轻松聊天 & 情绪价值\n"
        f"🔥 技术陪玩｜稳定上分 & 指导\n\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👩‍🚀可自助下单/到接待大厅联系客服/私信客服！\n"
        f"✨希望板板在 EESTUDIO 能找到属于您的快乐！\n"
        f"➤[⁠「🌸接待大厅」](https://discord.com/channels/1094496767329960016/1094496767988469815)\n"
        f"➤[📠-自助下单](https://discord.com/channels/1094496767329960016/1559560863734698056)"

    )
    embed.set_thumbnail(url=member.display_avatar.url)
    

    if channel:
        await channel.send(f"💝 欢迎您来到✨ 𝓔𝓔.𝓼𝓽𝓾𝓭𝓲𝓸 ✨ !, {member.mention}!", embed=embed)

class WelcomeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Get Started",
        style=discord.ButtonStyle.primary,
        emoji="🚀",
        custom_id="welcome:get_started",
    )
    async def get_started(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Welcome! Let's get you started.", ephemeral=True
        )

    @discord.ui.button(
        label="Who's online?",
        style=discord.ButtonStyle.secondary,
        emoji="📖",
        custom_id="welcome:learn_more",
    )
    async def learn_more(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Acknowledge first, then send everything as followups
        await interaction.response.defer(ephemeral=True)

        role = interaction.guild.get_role(STAFF_ROLE_ID)
        if role is None:
            await interaction.followup.send("Staff role not found.", ephemeral=True)
            return

        entries = get_online_staff(role)
        if not entries:
            await interaction.followup.send(
                "No staff members are online right now.", ephemeral=True
            )
            return

        # One message per member (a message can only have one view)
        for embed, view in entries[:10]:
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)


class StaffView(discord.ui.View):
    def __init__(self, target_member: discord.Member):
        super().__init__(timeout=300)
        self.target_member = target_member

    @discord.ui.button(
        label="Request",
        style=discord.ButtonStyle.primary,
        emoji="📩",
    )
    async def request(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.target_member.send(
                f"You have received a message request from "
                f"{interaction.user.display_name}!"
            )
            await interaction.response.send_message(
                f"Message sent to {self.target_member.display_name}!",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I couldn't DM this member. Their DMs may be disabled.",
                ephemeral=True,
            )


@bot.command()
@commands.has_permissions(administrator=True)
async def welcome(ctx):
    embed = discord.Embed(
        title="Welcome to Our Server!",
        description=(
            "We're glad to have you here! 🎉\n\n"
            "Click one of the buttons below to get started "
            "or learn more about our community."
        ),
        color=EMBED_COLOR,
    )
    member = ctx.guild.get_member(687499719127203850)
    embed.set_author(name="Your Server Name", icon_url=IMAGE_URL)
    embed.set_thumbnail(url=IMAGE_URL)
    embed.set_footer(text="Enjoy your stay!")
    embed.add_field(name=f"{member.display_name}'s Info", value=f"{member.mention}'s   [Card](https://discord.com/channels/1557939434018570260/1558444293213913088/1558444293213913088)")
    await ctx.send(embed=embed, view=WelcomeView())

@bot.command()
@commands.has_permissions(administrator=True)
async def servicerequest(ctx):
    embed = discord.Embed(
        title="欢迎来到 EE.STUDIO! 🎉",
        description=(
            "很开心你加入我们～"
            "点击下方按钮提交服务需求，或了解更多社群资讯。"
            "希望你在这里玩得开心，找到喜欢的伙伴！"
        ),
        color=EMBED_COLOR,
    )
    embed.set_author(name="Your Server Name", icon_url=IMAGE_URL)
    embed.set_thumbnail(url=IMAGE_URL)
    embed.set_footer(text="Enjoy your stay!")

    await ctx.send(embed=embed, view=ServiceRequestView())

def get_online_staff(role: discord.Role):
    """Return a list of (embed, view) for each non-offline, non-bot member of the role."""
    entries = []

    for member in role.members:
        if member.bot or member.status == discord.Status.offline:
            continue

        status = member.status.name
        emoji = STATUS_EMOJI.get(status, "⚪")

        embed = discord.Embed(
            title=member.display_name,
            description=f"{emoji} {status}",
            color=EMBED_COLOR,
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        entries.append((embed, StaffView(target_member=member)))

    return entries




bot.run(os.getenv("DISCORD_TOKEN"))