import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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
    if dt <= now:  # already passed today, so assume tomorrow
        dt += timedelta(days=1)
    return dt
