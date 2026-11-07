import discord

from bot.config import EMBED_COLOR
from bot.views.registration import RegistrationModal

CGameOptions = [
    discord.SelectOption(label="Valorant娱乐", value="Valorant娱乐"),
    discord.SelectOption(label="Valorant技术", value="Valorant技术"),
    discord.SelectOption(label="Apex娱乐", value="Apex娱乐"),
    discord.SelectOption(label="Apex技术", value="Apex技术"),
    discord.SelectOption(label="CS2娱乐", value="CS2娱乐"),
    discord.SelectOption(label="CS2技术", value="CS2技术"),
    discord.SelectOption(label="LOL娱乐", value="LOL娱乐"),
    discord.SelectOption(label="LOL技术", value="LOL技术"),
    discord.SelectOption(label="三角洲", value="三角洲"),
    discord.SelectOption(label="Steam", value="Steam"),
]
MGameOptions = [
    discord.SelectOption(label="王者荣耀", value="王者荣耀"),
    discord.SelectOption(label="HOK", value="HOK"),
]
TimeOptions = [
    discord.SelectOption(label="1 小时", value="1 小时"),
    discord.SelectOption(label="2 小时", value="2 小时"),
    discord.SelectOption(label="3 小时", value="3 小时"),
]
GenderOptions = [
    discord.SelectOption(label="男陪", value="男陪"),
    discord.SelectOption(label="女陪", value="女陪"),
    discord.SelectOption(label="不限", value="不限"),
]


def make_embed(title: str) -> discord.Embed:
    return discord.Embed(title=title, color=EMBED_COLOR)


# ---------------------------------------------------------------- Step 1
class ServiceType(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    async def _next(self, interaction: discord.Interaction, service_type: str):
        await interaction.response.edit_message(
            embed=make_embed("设备种类"),
            view=DeviceType(serviceType=service_type),
        )

    @discord.ui.button(label="陪玩", style=discord.ButtonStyle.primary, emoji="🎮")
    async def serviceGame(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._next(interaction, "陪玩")

    @discord.ui.button(label="陪聊", style=discord.ButtonStyle.primary, emoji="💬")
    async def serviceChat(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Chat needs neither a device nor a game, so skip the device step
        await interaction.response.edit_message(
            embed=make_embed("您的要求"),
            view=GamesPreferences(serviceType="陪聊", deviceType=None),
        )


# ---------------------------------------------------------------- Step 2
class DeviceType(discord.ui.View):
    def __init__(self, serviceType: str):
        super().__init__(timeout=60)
        self.serviceType = serviceType

    async def _next(self, interaction: discord.Interaction, device_type: str):
        await interaction.response.edit_message(
            embed=make_embed("您的要求"),
            view=GamesPreferences(
                serviceType=self.serviceType,
                deviceType=device_type,
            ),
        )

    @discord.ui.button(label="电脑", style=discord.ButtonStyle.primary, emoji="💻")
    async def deviceComputer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._next(interaction, "电脑")

    @discord.ui.button(label="手机", style=discord.ButtonStyle.primary, emoji="📱")
    async def deviceMobile(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._next(interaction, "手机")


# ---------------------------------------------------------------- Step 3
class GameSelect(discord.ui.Select):
    def __init__(self, parent: "GamesPreferences"):
        self.prefs = parent
        options = CGameOptions if self.prefs.deviceType == "电脑" else MGameOptions
        super().__init__(placeholder="选择一个游戏...", options=options, row=0)

    async def callback(self, interaction: discord.Interaction):
        self.prefs.selected_game = self.values[0]
        await interaction.response.defer()


class TimeSelect(discord.ui.Select):
    def __init__(self, parent: "GamesPreferences"):
        self.prefs = parent
        super().__init__(placeholder="选择一个时间...", options=TimeOptions, row=1)

    async def callback(self, interaction: discord.Interaction):
        self.prefs.selected_time = self.values[0]
        await interaction.response.defer()


class GenderSelect(discord.ui.Select):
    def __init__(self, parent: "GamesPreferences"):
        self.prefs = parent
        super().__init__(placeholder="选择一个性别...", options=GenderOptions, row=2)

    async def callback(self, interaction: discord.Interaction):
        self.prefs.selected_gender = self.values[0]
        await interaction.response.defer()


class GamesPreferences(discord.ui.View):
    def __init__(self, serviceType: str, deviceType: str | None):
        super().__init__(timeout=60)
        self.serviceType = serviceType
        self.deviceType = deviceType

        self.selected_game = None
        self.selected_time = None
        self.selected_gender = None

        # Chat service has no game, so only show the game select for 陪玩
        self.needs_game = serviceType == "陪玩"
        if self.needs_game:
            self.add_item(GameSelect(self))
        self.add_item(TimeSelect(self))
        self.add_item(GenderSelect(self))

    @discord.ui.button(label="确认选项", style=discord.ButtonStyle.success, row=3)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        required = [self.selected_time, self.selected_gender]
        if self.needs_game:
            required.append(self.selected_game)

        if not all(required):
            await interaction.response.send_message(
                f"请选择选项", ephemeral=True
            )
            return

        await interaction.response.send_modal(
            RegistrationModal(
                serviceType=self.serviceType,
                deviceType=self.deviceType,  # None for 陪聊
                selected_game=self.selected_game,  # None for 陪聊
                selected_time=self.selected_time,
                selected_gender=self.selected_gender,
            )
        )
