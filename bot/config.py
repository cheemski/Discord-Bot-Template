# Shared constants — replace every placeholder with your server values.

# Role / channel IDs (Discord snowflakes)
STAFF_ROLE_ID = 0  # YOUR_STAFF_ROLE_ID
WELCOME_CHANNEL_ID = 0  # YOUR_WELCOME_CHANNEL_ID
GUILD_ID = 0  # YOUR_GUILD_ID
CATEGORY_ID = 0  # YOUR_TICKET_CATEGORY_ID
MOD_ROLE_ID = 0  # YOUR_MOD_ROLE_ID
MOD_CHANNEL_ID = 0  # YOUR_MOD_CHANNEL_ID
SHOWCASE_MEMBER_ID = 0  # YOUR_SHOWCASE_MEMBER_ID
BASE_MATCH_ROLE_ID = 0  # YOUR_BASE_MATCH_ROLE_ID (always required when confirming)

# Branding / display
SERVER_NAME = "YOUR_SERVER_NAME"
EMBED_COLOR = 0x000000  # YOUR_EMBED_COLOR (e.g. 0xFFB7C5)
IMAGE_URL = "YOUR_IMAGE_URL"
MAX_COUNT = 5  # max companions per order

STATUS_EMOJI = {"online": "🟢", "idle": "🟡", "dnd": "🔴"}

# Channel / message links (must be valid https URLs for Discord link buttons)
LOBBY_CHANNEL_URL = "https://discord.com/channels/YOUR_GUILD_ID/YOUR_LOBBY_CHANNEL_ID"
SELF_ORDER_CHANNEL_URL = "https://discord.com/channels/YOUR_GUILD_ID/YOUR_SELF_ORDER_CHANNEL_ID"
PRICES_CHANNEL_URL = "https://discord.com/channels/YOUR_GUILD_ID/YOUR_PRICES_CHANNEL_ID"
PAYMENT_QR_URL = "https://discord.com/channels/YOUR_GUILD_ID/YOUR_CHANNEL_ID/YOUR_MESSAGE_ID"
SHOWCASE_CARD_URL = "https://discord.com/channels/YOUR_GUILD_ID/YOUR_CHANNEL_ID/YOUR_MESSAGE_ID"

# Game name → Discord role ID
GAME_ROLES = {
    "CS2娱乐": 0,  # YOUR_CS2_CASUAL_ROLE_ID
    "CS2技术": 0,  # YOUR_CS2_TECH_ROLE_ID
    "Valorant娱乐": 0,  # YOUR_VALORANT_CASUAL_ROLE_ID
    "Valorant技术": 0,  # YOUR_VALORANT_TECH_ROLE_ID
    "Apex娱乐": 0,  # YOUR_APEX_CASUAL_ROLE_ID
    "Apex技术": 0,  # YOUR_APEX_TECH_ROLE_ID
    "LOL娱乐": 0,  # YOUR_LOL_CASUAL_ROLE_ID
    "LOL技术": 0,  # YOUR_LOL_TECH_ROLE_ID
    "三角洲": 0,  # YOUR_DELTAFORCE_ROLE_ID
}

# Gender preference → Discord role ID
GENDER_ROLES = {
    "男陪": 0,  # YOUR_MALE_STAFF_ROLE_ID
    "女陪": 0,  # YOUR_FEMALE_STAFF_ROLE_ID
    "不限": 0,  # YOUR_ANY_GENDER_ROLE_ID
}

# staff user ID → profile card message link
STAFF_CARD = {
    # 0: "https://discord.com/channels/YOUR_GUILD_ID/YOUR_CHANNEL_ID/YOUR_MESSAGE_ID",  # example
}
