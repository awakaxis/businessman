import discord

class Debug:

    @staticmethod
    def page_debug(content):
        embed = discord.Embed(title="Auction results:")

        for element in [content["auctions"][i] for i in range(0, 24)]:
            embed.add_field(name="", value=element["item_name"], inline=False)
        return embed
    

class User:

    @staticmethod
    def basic_bin_price_list(content, item_name, amt: int = 10):
        title = str.format("{0} lowest bins", item_name)
        embed = discord.Embed(title=title)

        for i in range(0, amt):
            item = content[i]
            embed.add_field(name="", value= str.format("{0}. {1} - {2} Coins", i+1, item["item_name"], item["starting_bid"]), inline=False)
        
        return embed
