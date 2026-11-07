import discord

from bot.config import EMBED_COLOR, STAFF_ROLE_ID, STATUS_EMOJI


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
