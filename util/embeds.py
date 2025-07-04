import discord


class Debug:

    @staticmethod
    def page_debug(content):
        embed = discord.Embed(title="Auction results:")

        for element in [content["auctions"][i] for i in range(0, 24)]:
            embed.add_field(name="", value=element["item_name"], inline=False)
        return embed
