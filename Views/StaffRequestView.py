import discord
from discord.ext import commands
import asyncio
import time
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

MAX_COUNT = 5

STAFF_CARD = {
    798839672679563285 : "https://discord.com/channels/1094496767329960016/1558533881613914122/1558533881613914122", # monzy
    403530878459838464 : "https://discord.com/channels/1094496767329960016/1546752293590794401/1546752293590794401", # ron
    707852605711188000 : "https://discord.com/channels/1094496767329960016/1522087326443110400/1522087326443110400", # July
    443069557746171915 : "https://discord.com/channels/1094496767329960016/1534281794504097902/1534281794504097902", #雪yu
    897401512265912322 : "https://discord.com/channels/1094496767329960016/1553724565912289330/1553724565912289330", #啊彬
    665439683341320193 : "https://discord.com/channels/1094496767329960016/1521727843833221233/1521727843833221233", #muffin
    335592360115175425 : "https://discord.com/channels/1094496767329960016/1521727706461376573/1521727706461376573", #markl
    693252175828353044 : "https://discord.com/channels/1094496767329960016/1521841689902317605/1521841689902317605", #reach
    788916445043490858 : "https://discord.com/channels/1094496767329960016/1534283743064363119/1534283743064363119", #啊乐
    233630392073191424 : "https://discord.com/channels/1094496767329960016/1534283617402884259/1534283617402884259", #CT
    943016124486938656 : "https://discord.com/channels/1094496767329960016/1521562901062746122/1521562901062746122", #阿正
    850105412911890492 : "https://discord.com/channels/1094496767329960016/1529438199242428637/1529438199242428637", #G9 
    680332536102256648 : "https://discord.com/channels/1094496767329960016/1527030057401450649/1527030057401450649", #laogao
    798839672679563285 : "https://discord.com/channels/1094496767329960016/1527029959498006679/1527029959498006679", #Ivix ？？？
    287951289059377153 : "https://discord.com/channels/1094496767329960016/1521727952377614487/1521727952377614487", #卡卡西
    857461867428446248 : "https://discord.com/channels/1094496767329960016/1521842920762904726/1521842920762904726", #luzifer
    901194519578546197 : "https://discord.com/channels/1094496767329960016/1521727213425397840/1521727213425397840", #gib
    392313920347701248 : "https://discord.com/channels/1094496767329960016/1521727593529737286/1521727593529737286", #ken ？？？
    328536859095465991 : "https://discord.com/channels/1094496767329960016/1521727122886885376/1521727122886885376", #chris
    459723961324929024 : "https://discord.com/channels/1094496767329960016/1521728203360571503/1521728203360571503", #小圣
    869013084398817300 : "https://discord.com/channels/1094496767329960016/1521727503238959105/1521727503238959105", #jimmy
    369450202580516874 : "https://discord.com/channels/1094496767329960016/1521727423085936670/1521727423085936670", #golden
    1301187222091075626 : "https://discord.com/channels/1094496767329960016/1521746697406124133/1521746697406124133", #小薰
    992076691117723718 : "https://discord.com/channels/1094496767329960016/1521759204208279707/1521759204208279707", #森77
    1492114598822678660 : "https://discord.com/channels/1094496767329960016/1521746505948467251/1521746505948467251", #lele
    1146505235708268727 : "https://discord.com/channels/1094496767329960016/1534282060531892384/1534282060531892384", #凌玖
    816380400321953804 : "https://discord.com/channels/1094496767329960016/1558534138250657894/1558534138250657894", #柚子 
    1146898477750698115 : "https://discord.com/channels/1094496767329960016/1558534024933277758/1558534024933277758", #r7ieo
    698212123074887810 : "https://discord.com/channels/1094496767329960016/1553723186183675984/1553723186183675984", #夕夕
    523193172323729410 : "https://discord.com/channels/1094496767329960016/1529435944208306299/1529435944208306299", #娜娜
    814904338488623114 : "https://discord.com/channels/1094496767329960016/1527029344105533610/1527029344105533610", #凌凌
    517002741143568384 : "https://discord.com/channels/1094496767329960016/1521836358165987480/1521836358165987480", #kambe
    1146465021359030392 : "https://discord.com/channels/1094496767329960016/1521802022855245907/1521802022855245907", #小姚
    894925034949320704 : "https://discord.com/channels/1094496767329960016/1553723529357172806/1553723529357172806", #四脚蛇
    1542172521837625471 : "https://discord.com/channels/1094496767329960016/1553724461738500096/1553724461738500096", #wen 
    1550117182250295413 : "https://discord.com/channels/1094496767329960016/1553723893418692638/1553723893418692638", #小晴 
    995898132397309953 : "https://discord.com/channels/1094496767329960016/1553723702687039548/1553723702687039548", #芒果
    799151452227764235 : "https://discord.com/channels/1094496767329960016/1521759349700300953/1521759349700300953", #西西
    739236737988952145 : "https://discord.com/channels/1094496767329960016/1521759473839116298/1521759473839116298", #小k
    721645043244597288 : "https://discord.com/channels/1094496767329960016/1534282760934658098/1534282760934658098", #草草
    772075345029103626 : "https://discord.com/channels/1094496767329960016/1534282296897699901/1534282296897699901", #空翌
    829637664146849793 : "https://discord.com/channels/1094496767329960016/1534639131609530540/1534639131609530540", #伊奈
    1369759180617023630 : "https://discord.com/channels/1094496767329960016/1521853840708604066/1521853840708604066", #六六
    419943667726549003 : "https://discord.com/channels/1094496767329960016/1546753252874260511/1546753252874260511", #玛卡
    1516488625955672195 : "https://discord.com/channels/1094496767329960016/1542933292062478388/1542933292062478388", #小颖
    499222896590192641 : "https://discord.com/channels/1094496767329960016/1521758585023889469/1521758585023889469", #狐狐
    728668741428314203 : "https://discord.com/channels/1094496767329960016/1542932949169610802/1542932949169610802", #酸菜鱼
    719366481585897522 : "https://discord.com/channels/1094496767329960016/1521746224196096041/1521746224196096041", #zero
    1517554534560567457 : "https://discord.com/channels/1094496767329960016/1521863845151375370/1521863845151375370", #七月
    713034910771970049 : "https://discord.com/channels/1094496767329960016/1534385841005138052/1534385841005138052", #阿九
    1516124470866219078 : "https://discord.com/channels/1094496767329960016/1542934449547780297/1542934449547780297", #Harry
    360739309147521025 : "https://discord.com/channels/1094496767329960016/1542933110503514273/1542933110503514273", #黑猫
    873990733936345118 : "https://discord.com/channels/1094496767329960016/1529440777837482054/1529440777837482054", #ad
    1193911268403335170 : "https://discord.com/channels/1094496767329960016/1529435510974578778/1529435510974578778", #花花 
    813639904751517706 : "https://discord.com/channels/1094496767329960016/1521770374700863688/1521770374700863688", #丫蕥
    1145394897529090168 : "https://discord.com/channels/1094496767329960016/1521758410037792888/1521758410037792888", #烤鹅
    1425848281954779218 : "https://discord.com/channels/1094496767329960016/1529435788578787389/1529435788578787389", #旺仔
    716963103794921574 : "https://discord.com/channels/1094496767329960016/1521840881903075359/1521840881903075359", #峻
    856017439699894282 : "https://discord.com/channels/1094496767329960016/1521758300625043516/1521758300625043516", #晚安
    699518770405834762 : "https://discord.com/channels/1094496767329960016/1527028796799189112/1527028796799189112", #卖佬
    772330134647865424 : "https://discord.com/channels/1094496767329960016/1527029542387191879/1527029542387191879", #时行
    1487430033143234681 : "https://discord.com/channels/1094496767329960016/1527029081986568193/1527029081986568193", #zoe
    954034076296314940 : "https://discord.com/channels/1094496767329960016/1521747737979388004/1521747737979388004", #巧恩
    810552067113746523 : "https://discord.com/channels/1094496767329960016/1521759055838843002/1521759055838843002", #皮蛋
    806402973148250123 : "https://discord.com/channels/1094496767329960016/1521758901023014923/1521758901023014923", #白也
    889442589202350110 : "https://discord.com/channels/1094496767329960016/1521758818848083978/1521758818848083978", #猫猫
    509627133811884032 : "https://discord.com/channels/1094496767329960016/1521746934539227227/1521746934539227227", #小雪兔
    915168112813436988 : "https://discord.com/channels/1094496767329960016/1521745503388176486/1521745503388176486", #美禄冰
    713784414240374836 : "https://discord.com/channels/1094496767329960016/1521745179332317195/1521745179332317195", #Laowan
}
EMBED_COLOR = 0xFFB7C5
MOD_ROLE_ID = 1483828119210168474
MOD_CHANNEL_ID = 1558892554609491988
TZ = ZoneInfo("Asia/Kuala_Lumpur")
def parse_time(text: str) -> datetime | None:
    text = text.strip().lower()
    now = datetime.now(TZ)

    if text in ("现在", "now", "asap"):
        return now

    m = re.fullmatch(r"(\d{1,2})(?:[:：.](\d{2}))?\s*(am|pm)?", text)
    if not m:
        return None

    hour, minute, ampm = int(m[1]), int(m[2] or 0), m[3]
    if ampm == "pm" and hour < 12:
        hour += 12
    elif ampm == "am" and hour == 12:
        hour = 0
    if hour > 23 or minute > 59:
        return None

    dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if dt <= now:               # already passed today, so assume tomorrow
        dt += timedelta(days=1)
    return dt

class RequestState:
    """Shared between the user's ephemeral message and the mod channel message."""

    def __init__(self, user_interaction, requester, ticket_channel, roles: list[int], message, user_rank, length, time_chosen, count: int = 1, steam_game: str | None = None):
        self.user_interaction = user_interaction
        self.requester = requester
        self.ticket_channel = ticket_channel
        self.roles = roles
        self.volunteers: dict[int, discord.Member] = {}
        self.volunteer_time : dict[int, str] = {}
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
        view = ChooseView(self) if ready else None   # hidden until enough volunteers
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

        s.settled = True                      # set early so a second click can't slip in
        await interaction.response.defer()    # acknowledge within 3 seconds

        try:
            ticket_no = await interaction.client.pool.fetchval(
                "INSERT INTO settled_tickets (staff_ids, requester_id) VALUES ($1, $2) RETURNING id",
                [m.id for m in s.chosen], s.requester.id,
            )
        except Exception:
            s.settled = False                 # allow a retry if the insert failed
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
        if len(chosen) != len(ids):   # someone withdrew just before the pick
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
            except discord.HTTPException:   # includes Forbidden
                failed.append(m)

        if failed:
            await s.ticket_channel.send(
                "⚠️ 无法给以下陪陪开放权限，请管理员手动处理: "
                + " ".join(m.mention for m in failed)
            )

        await s.ticket_channel.send(
            f"{mentions} 被选中接待 {s.requester.mention}.\n"
            f"稍等片刻，客服会和板板确认价格的事宜！\n"
            f"然后板板麻烦移步到 [QR CODE](https://discord.com/channels/1094496767329960016/1559557136499871805/1559557221845700618)进行付款\n"
            f"付款成功后，麻烦请把付记录发在这里让客服检查呀~"
        )


class ChooseView(discord.ui.View):
    def __init__(self, state: RequestState):
        super().__init__(timeout=900)
        self.add_item(ChooseSelect(state))