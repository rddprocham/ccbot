import discord
from discord.ext import commands

class Tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Ping command
    @commands.command(
            aliases = ['p'],
            help = "Useful to check if the bot is on, able to read/send messages, as well as see the latency",
            description = "Returns pong and bot latency",
            brief = "Returns pong and bot latency",
    )
    async def ping(self, ctx):
        await ctx.send(f"Pong! Bot latency is {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def dmping(self, ctx):
        dm = await ctx.message.author.create_dm()
        await dm.send(f"Pong! Bot latency is {round(self.bot.latency * 1000)}ms")

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

async def setup(bot):
    await bot.add_cog(Tests(bot=bot))