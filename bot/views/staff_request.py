import time

import discord

from bot.config import EMBED_COLOR, MAX_COUNT, MOD_ROLE_ID, PAYMENT_QR_URL, STAFF_CARD
from bot.utils.time_parse import parse_time

# Re-export for callers that previously imported MAX_COUNT from this module
__all__ = [
    "MAX_COUNT",
    "RequestState",
    "ModView",
    "ModConfirmView",
    "ModModal",
    "ChooseSelect",
    "ChooseView",
]


class RequestState:
    """Shared between the user's ephemeral message and the mod channel message."""

    def __init__(
        self,
        user_interaction,
        requester,
        ticket_channel,
        roles: list[int],
        message,
        user_rank,
        length,
        time_chosen,
        count: int = 1,
        steam_game: str | None = None,
    ):
        self.user_interaction = user_interaction
        self.requester = requester
        self.ticket_channel = ticket_channel
        self.roles = roles
        self.volunteers: dict[int, discord.Member] = {}
        self.volunteer_time: dict[int, str] = {}
        self.mod_message: discord.Message | None = None
        self.user_rank = user_rank
        self.message = message
        self.closed = False
        self.length = length
        self.created = time.time()
        self.time_chosen = time_chosen
        self.count = count
        self.chosen: list[discord.Member] = []
        self.settled = False
        self.steam_game = steam_game

    @property
    def active(self) -> bool:
        # stops counting as pending once the interaction token (15 min) is nearly dead
        return not self.closed and time.time() - self.created < 14 * 60

    def _volunteer_lines(self) -> str:
        lines = []
        for m in self.volunteers.values():
            card = STAFF_CARD.get(m.id)
            who = f"{m.mention} [card]({card})" if card else m.mention
            lines.append(f"• {who} (接单时间: {self.volunteer_time.get(m.id, '未填')})")
        return "\n".join(lines)

    def user_embed(self) -> discord.Embed:
        embed = discord.Embed(title="Your request", color=EMBED_COLOR)
        n = len(self.volunteers)

        if n >= self.count:
            embed.description = f"已有 {n} 位陪陪接单啦，请选择 {self.count} 位"
        elif n > 0:
            embed.description = f"需要 {self.count} 位陪陪，目前 {n}/{self.count} 位接单，请稍等..."
        else:
            embed.description = "请稍等片刻让陪陪们扣单..."

        if self.volunteers:
            embed.add_field(name="目前可接单", value=self._volunteer_lines(), inline=False)
        return embed

    def mod_embed(self, chosen: discord.Member | None = None) -> discord.Embed:
        desc = (
            f"**需求标签:** {', '.join(f'{r.mention}' for r in self.roles)}\n"
            f"**板板:** {self.requester.mention}\n"
            f"**自介:** {self.ticket_channel.mention}\n"
            f"**约时:** {self.time_chosen}\n"
            f"**时长:** {self.length}\n"
        )
        if self.steam_game:
            desc += f"**Steam 游戏:** {self.steam_game}\n"
        else:
            desc += f"**段位:** {self.user_rank}\n"
        desc += (
            f"**备注:** {self.message}\n"
            f"**人数:** {self.count}\n"
        )

        embed = discord.Embed(
            title="新的单来啦！ (๑•̀ㅂ•́)و✧",
            description=desc,
            color=EMBED_COLOR,
        )
        embed.add_field(
            name="接单情况",
            value=self._volunteer_lines() or "目前还没有人接单哦～",
            inline=False,
        )
        if chosen:
            embed.add_field(name="陪陪", value=" ".join(m.mention for m in chosen), inline=False)
        return embed

    async def refresh_user(self):
        ready = len(self.volunteers) >= self.count
        view = ChooseView(self) if ready else None  # hidden until enough volunteers
        try:
            await self.user_interaction.edit_original_response(
                embed=self.user_embed(), view=view
            )
        except discord.HTTPException:
            pass


class ModView(discord.ui.View):
    def __init__(self, state: RequestState):
        super().__init__(timeout=None)
        self.state = state

    @discord.ui.button(label="我来接单🙋‍♀️", style=discord.ButtonStyle.success, emoji="🙋")
    async def volunteer(self, interaction: discord.Interaction, button: discord.ui.Button):
        s = self.state
        if not all(role in interaction.user.roles for role in s.roles):
            return await interaction.response.send_message("Not for you.", ephemeral=True)
        if s.closed:
            return await interaction.response.send_message("This ticket is closed.", ephemeral=True)

        # pressing again withdraws
        if interaction.user.id in s.volunteers:
            del s.volunteers[interaction.user.id]
            s.volunteer_time.pop(interaction.user.id, None)
            await interaction.response.edit_message(embed=s.mod_embed(), view=self)
            return await s.refresh_user()

        # otherwise ask for a time; they're only added when the modal is submitted
        await interaction.response.send_modal(ModModal(s, self))


class ModConfirmView(discord.ui.View):
    def __init__(self, state: RequestState):
        super().__init__(timeout=None)
        self.state = state

    @discord.ui.button(label="确认单", style=discord.ButtonStyle.success, emoji="✅")
    async def confirmTicket(self, interaction: discord.Interaction, button: discord.ui.Button):
        s = self.state
        if interaction.user.get_role(MOD_ROLE_ID) is None:
            return await interaction.response.send_message("Not for you.", ephemeral=True)
        if s.settled:
            return await interaction.response.send_message("这张单已经确认过了。", ephemeral=True)

        s.settled = True  # set early so a second click can't slip in
        await interaction.response.defer()  # acknowledge within 3 seconds

        try:
            ticket_no = await interaction.client.pool.fetchval(
                "INSERT INTO settled_tickets (staff_ids, requester_id) VALUES ($1, $2) RETURNING id",
                [m.id for m in s.chosen], s.requester.id,
            )
        except Exception:
            s.settled = False  # allow a retry if the insert failed
            raise

        embed = s.mod_embed(s.chosen)
        embed.title = f"单号DD{ticket_no}"
        await interaction.edit_original_response(embed=embed, view=None)


class ModModal(discord.ui.Modal, title="时间"):
    def __init__(self, state: RequestState, view: ModView):
        super().__init__()
        self.state = state
        self.view = view

        self.set_time = discord.ui.TextInput(
            label="几点开始？（马来西亚时间）",
            placeholder="例如 20:30 / 8:30pm / 现在",
            max_length=10,
        )
        self.add_item(self.set_time)

    async def on_submit(self, interaction: discord.Interaction):
        s = self.state
        if s.closed:
            return await interaction.response.send_message("This ticket is closed.", ephemeral=True)

        dt = parse_time(self.set_time.value)
        if dt is None:
            return await interaction.response.send_message(
                "时间格式不对，请用 20:30 或 8:30pm 这样的格式。", ephemeral=True
            )

        s.volunteers[interaction.user.id] = interaction.user
        s.volunteer_time[interaction.user.id] = f"<t:{int(dt.timestamp())}:t>"

        await interaction.response.edit_message(embed=s.mod_embed(), view=self.view)
        await s.refresh_user()


class ChooseSelect(discord.ui.Select):
    def __init__(self, state: RequestState):
        self.state = state
        options = [
            discord.SelectOption(label=m.display_name[:100], value=str(m.id))
            for m in list(state.volunteers.values())[:25]
        ]
        super().__init__(
            placeholder=f"请选择 {state.count} 位陪陪",
            min_values=state.count,
            max_values=state.count,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        s = self.state
        if s.closed:
            return await interaction.response.send_message("已经确认.", ephemeral=True)

        ids = [int(v) for v in self.values]
        chosen = [s.volunteers[i] for i in ids if i in s.volunteers]
        if len(chosen) != len(ids):  # someone withdrew just before the pick
            await interaction.response.send_message(
                "有陪陪暂时不得空，请重新选择。", ephemeral=True
            )
            return await s.refresh_user()

        s.closed = True
        mentions = " ".join(m.mention for m in chosen)
        s.chosen = chosen
        done = discord.Embed(
            title="确认!",
            description=f"{mentions} 会接待你.",
            color=EMBED_COLOR,
        )
        done.set_thumbnail(url=chosen[0].display_avatar.url)
        await interaction.response.edit_message(embed=done, view=None)

        if s.mod_message:
            try:
                await s.mod_message.edit(embed=s.mod_embed(chosen), view=None)
            except discord.HTTPException:
                pass

        overwrite = discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True,
            embed_links=True,
        )

        failed = []
        for m in chosen:
            try:
                await s.ticket_channel.set_permissions(
                    m, overwrite=overwrite, reason="Chosen for ticket"
                )
            except discord.HTTPException:  # includes Forbidden
                failed.append(m)

        if failed:
            await s.ticket_channel.send(
                "⚠️ 无法给以下陪陪开放权限，请管理员手动处理: "
                + " ".join(m.mention for m in failed)
            )

        await s.ticket_channel.send(
            f"{mentions} 被选中接待 {s.requester.mention}.\n"
            f"稍等片刻，客服会和板板确认价格的事宜！\n"
            f"然后板板麻烦移步到 [QR CODE]({PAYMENT_QR_URL})进行付款\n"
            f"付款成功后，麻烦请把付记录发在这里让客服检查呀~"
        )


class ChooseView(discord.ui.View):
    def __init__(self, state: RequestState):
        super().__init__(timeout=900)
        self.add_item(ChooseSelect(state))
