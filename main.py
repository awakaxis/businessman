import os
from logging import Logger

import discord
from discord import ApplicationContext, Intents, SlashCommandGroup
from discord.ext import commands

import util.request_helper as request_helper
from util import request_helper
from util.embeds import Debug
from util.embeds import User
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

        @self.slash_command()
        async def getauctions(ctx: ApplicationContext, name: str):
            await ctx.defer()

            items = request_helper.get_auctions_by_item(name, True)
            final = ""

            for item in items:
                final = (
                    final
                    + "Price: "
                    + str(item["starting_bid"])
                    + item["item_name"]
                    + "\n"
                )

            await ctx.send_followup(final)
            # channel =  await self.fetch_channel(ctx.channel_id)

            # for split in [final[i:i + 2000] for i in range(0, len(final), 2000)]:
            #    await channel.send(split)

        @self.slash_command()
        async def lowestbin(ctx: ApplicationContext, item_name: str, amount_to_show: int = 10):
            await ctx.defer()

            item_list = request_helper.get_auctions_by_item(item_name, True)
            top_n = request_helper.get_lowest_n(item_list, amount_to_show)

            embed = User.basic_bin_price_list(top_n, item_name, amount_to_show)
            await ctx.send_followup(embed=embed)

        debug: SlashCommandGroup = self.create_group(
            name="debug", description="debug commands"
        )

        @debug.command()
        async def get_page_count(ctx: ApplicationContext):
            result = request_helper.get_total_page_count()
            await ctx.respond(result)

        @debug.command()
        async def get_page(ctx: ApplicationContext, page_number: int):
            result = request_helper.get_auction_page_json(page_number)
            embed = Debug.page_debug(result)
            await ctx.respond(embed=embed)

bot = BusinessMan(get_logger("Businessman"))

bot.run(TOKEN)
