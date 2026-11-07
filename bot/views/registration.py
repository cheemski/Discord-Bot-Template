import asyncio

import discord

from bot.config import (
    BASE_MATCH_ROLE_ID,
    CATEGORY_ID,
    EMBED_COLOR,
    GAME_ROLES,
    GENDER_ROLES,
    MAX_COUNT,
    MOD_CHANNEL_ID,
    MOD_ROLE_ID,
    PRICES_CHANNEL_URL,
)
from bot.utils.time_parse import parse_time
from bot.views.staff_request import ModView, RequestState


class RegistrationModal(discord.ui.Modal, title="您的要求"):
    def __init__(self, serviceType, deviceType, selected_game, selected_time, selected_gender):
        super().__init__()
        self.serviceType = serviceType
        self.deviceType = deviceType
        self.selected_game = selected_game
        self.selected_time = selected_time
        self.selected_gender = selected_gender
        self.time_input = None

        # 陪聊 (chat) has no rank, so only add the rank input for 陪玩
        self.is_chat = serviceType == "陪聊"
        self.is_steam = selected_game == "Steam"

        self.rank = None
        self.steam_game = None

        if self.is_steam:
            self.steam_game = discord.ui.TextInput(
                label="Steam 游戏名称",
                placeholder="例如 Dota 2 / PUBG",
                required=True,
                max_length=50,
            )
            self.add_item(self.steam_game)
        elif not self.is_chat:
            self.rank = discord.ui.TextInput(
                label="段位",
                placeholder="e.g GOLD, PLAT",
                required=True,
                max_length=10,
            )
            self.add_item(self.rank)

        self.preferences = discord.ui.TextInput(
            label="备注",
            placeholder="特别需求",
            required=True,
            max_length=100,
        )
        self.add_item(self.preferences)

        self.time_input = discord.ui.TextInput(
            label="几点开始？（马来西亚时间）",
            placeholder="例如 20:30 / 8:30pm / 现在",
            max_length=10,
        )
        self.add_item(self.time_input)

        self.count_input = discord.ui.TextInput(
            label=f"需要几位陪陪？（1-{MAX_COUNT}）",
            placeholder="例如 1",
            default="1",
            max_length=2,
        )
        self.add_item(self.count_input)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user

        if guild is None:
            return

        existing = discord.utils.get(
            guild.text_channels,
            topic=f"ticket_owner:{user.id}",
        )

        if existing:
            await interaction.response.send_message(
                f"You already have a ticket: {existing.mention}",
                ephemeral=True,
            )
            return

        category = guild.get_channel(CATEGORY_ID)
        mod_role = guild.get_role(MOD_ROLE_ID)

        if not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message(
                "Ticket category not found.",
                ephemeral=True,
            )
            return

        if mod_role is None:
            await interaction.response.send_message(
                "Moderator role not found.",
                ephemeral=True,
            )
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),
            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True,
            ),
            mod_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_channels=True,
            ),
        }
        dt = parse_time(self.time_input.value)
        if dt is None:
            return await interaction.response.send_message(
                "时间格式不对，请用 20:30 或 8:30pm 这样的格式。", ephemeral=True
            )
        raw = self.count_input.value.strip()
        if not raw.isdigit() or not (1 <= int(raw) <= MAX_COUNT):
            return await interaction.response.send_message(
                f"人数请输入 1 到 {MAX_COUNT} 之间的整数。", ephemeral=True
            )
        count = int(raw)
        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}".lower()[:90],
            category=category,
            overwrites=overwrites,
            topic=f"ticket_owner:{user.id}",
        )

        # Build the info lines; chat tickets leave out device, game and rank
        lines = [f"- 服务类型: {self.serviceType}"]
        if not self.is_chat:
            lines.append(f"- 设备类型: {self.deviceType}")
            if self.is_steam:
                lines.append(f"- 选择的游戏: Steam（{self.steam_game.value}）")
            else:
                lines.append(f"- 选择的游戏: {self.selected_game}")
        lines.append(f"- 选择时长: {self.selected_time}")
        lines.append(f"- 选择约时: {self.time_input.value}")
        lines.append(f"- 陪陪人数: {count}")
        lines.append(f"- 选择性别: {self.selected_gender}")
        if self.rank:
            lines.append(f"- 段位: {self.rank.value}")
        lines.append(f"- 偏好: {self.preferences.value}")

        embed = discord.Embed(
            title="工单已创建",
            description=(
                f"你好 {user.mention},\n\n"
                "谢谢你来找我们！管理员很快就会来帮你啦～\n\n"
                "麻烦确认以下要求有满足板板的要求呀 ：\n"
                + "\n".join(lines)
                + "\n\n确认没问题的话，点击下方的 「确认资料」 就可以啦～"
                + "\n\n管理员很快来陪你处理！(๑˃̵ᴗ˂̵)و"
            ),
            color=EMBED_COLOR,
        )

        await channel.send(
            content=f"{user.mention} {mod_role.mention}",
            embed=embed,
            view=CloseTicketView(
                self.serviceType, self.selected_game, self.selected_gender,
                self.preferences.value,
                self.rank.value if self.rank else "无",
                self.selected_time,
                self.time_input.value,
                count,
                steam_game=self.steam_game.value if self.steam_game else None,
            ),
        )

        await interaction.response.send_message(
            f"Your ticket has been created: {channel.mention}",
            ephemeral=True,
        )


class CloseTicketView(discord.ui.View):
    def __init__(
        self,
        serviceType,
        selected_game,
        selected_gender,
        message,
        rank,
        selected_time,
        time_input,
        count,
        steam_game=None,
    ):
        super().__init__(timeout=None)
        self.serviceType = serviceType
        self.selected_game = selected_game
        self.selected_gender = selected_gender
        self.request: RequestState | None = None
        self.selected_time = selected_time
        self.rank = rank
        self.message = message
        self.time_input = time_input
        self.count = count
        self.steam_game = steam_game

        self.add_item(
            discord.ui.Button(
                label="Prices",
                style=discord.ButtonStyle.link,
                url=PRICES_CHANNEL_URL,
            )
        )

    @discord.ui.button(
        label="Confirm Details",
        emoji="✅",
        style=discord.ButtonStyle.primary,
        custom_id="ticket:confirm",
    )
    async def confirm_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        required = {
            BASE_MATCH_ROLE_ID,
            GAME_ROLES.get(self.selected_game),  # None for 陪聊
        }
        if not self.selected_gender == "不限":
            required.add(GENDER_ROLES.get(self.selected_gender))

        required.discard(None)  # ignore roles that don't apply
        required.discard(0)  # ignore unconfigured placeholders


        ##roles required
        roles = [interaction.guild.get_role(r) for r in required]

        ##state for both mod and user message
        state = RequestState(
            user_interaction=interaction,
            requester=interaction.user,
            ticket_channel=interaction.channel,
            roles=roles,
            message=self.message,
            user_rank=self.rank,
            length=self.selected_time,
            time_chosen=self.time_input,
            count=self.count,
            steam_game=self.steam_game,
        )
        self.request = state

        ##user message
        state.user_message = await interaction.response.send_message(embed=state.user_embed())

        ##mod message
        mod_channel = interaction.guild.get_channel(MOD_CHANNEL_ID)
        state.mod_message = await mod_channel.send(
            content=f"{', '.join(f'{r.mention}' for r in roles)}",
            embed=state.mod_embed(),
            view=ModView(state),
        )

    @discord.ui.button(
        label="Close Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="ticket:close",
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        channel = interaction.channel

        if not isinstance(channel, discord.TextChannel):
            return

        # Only the ticket owner or moderators can close it
        topic = channel.topic or ""
        is_owner = topic == f"ticket_owner:{interaction.user.id}"

        def check_mod(interaction: discord.Interaction):
            mod_role = interaction.guild.get_role(MOD_ROLE_ID)
            print(mod_role is not None)
            print(isinstance(interaction.user, discord.Member))
            print(mod_role in interaction.user.roles)

        mod_role = interaction.guild.get_role(MOD_ROLE_ID)
        is_mod = (
            mod_role is not None
            and isinstance(interaction.user, discord.Member)
            and mod_role in interaction.user.roles
        )

        if not (is_owner or is_mod):
            check_mod(interaction)
            await interaction.response.send_message(
                "You cannot close this ticket.",
                ephemeral=True,
            )
            return

        state = self.request
        if state is not None:
            state.closed = True  # also makes ChooseSelect / ModView bail out early
            if state.mod_message:
                try:
                    embed = state.mod_embed()
                    embed.set_footer(
                        text="工单已被关闭"
                    )
                    # view=None removes the 我来接单 button
                    await state.mod_message.edit(embed=embed, view=None)
                except discord.HTTPException:
                    pass  # message already deleted or edited away

        await interaction.response.send_message(
            "工单已被关闭, 将在 5 秒后删除频道"
        )

        await asyncio.sleep(5)
        await channel.delete(reason="Ticket closed")
