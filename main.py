import os
from logging import Logger

import discord
from discord import ApplicationContext, Intents
from discord.ext import commands

from util.log_helper import get_logger

TOKEN = os.getenv("BOT_TESTING_TOKEN")

client = discord.Client(intents=discord.Intents.all())

LOGGER = get_logger(__name__)


class BusinessMan(commands.Bot):
    def __init__(self, logger: Logger) -> None:
        super().__init__(command_prefix="^", intents=Intents.all())
        self.LOGGER = logger
        self.setup_commands()
        self.setup_application_commands()

    async def on_ready(self):
        self.LOGGER.info(f"Logged in as {self.user.name}")

    def setup_commands(self):
        @self.command()
        async def echo(ctx: commands.Context, message: str):
            await ctx.send(message)

    def setup_application_commands(self):
        @self.slash_command()
        async def echo(ctx: ApplicationContext, message: str):
            await ctx.respond(message)


bot = BusinessMan(get_logger("Businessman"))

bot.run(TOKEN)
