import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot.views.service_request import ServiceRequestView
from bot.views.welcome import WelcomeView

load_dotenv()

COGS = [
    "bot.cogs.events",
    "bot.cogs.welcome",
    "bot.cogs.service_request",
]


class MyBot(commands.Bot):
    async def setup_hook(self):
        # Register persistent buttons on startup
        self.add_view(WelcomeView())
        self.add_view(ServiceRequestView())

        for extension in COGS:
            await self.load_extension(extension)


def main():
    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True
    intents.message_content = True

    bot = MyBot(command_prefix="!", intents=intents)
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
