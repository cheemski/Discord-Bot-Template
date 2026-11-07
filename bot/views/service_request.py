import discord

from bot.config import EMBED_COLOR
from bot.views.request_flow import ServiceType


class ServiceRequestView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view with no timeout

    @discord.ui.button(
        label="提交下单需求",
        style=discord.ButtonStyle.primary,
        custom_id="service_request_button",
    )
    async def service_request_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="提交下单需求",
                description="请选择您需要的服务类型。",
                color=EMBED_COLOR,
            ),
            view=ServiceType(),
            ephemeral=True,
        )
