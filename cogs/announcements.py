import discord
from discord.ext import commands

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, what):
        await ctx.send(what)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

async def setup(bot):
    await bot.add_cog(Announcements(bot=bot))
