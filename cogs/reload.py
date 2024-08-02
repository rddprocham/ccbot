import discord
from discord.ext import commands

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Ping command
    @commands.command(aliases = ['r'])
    async def reload(self, ctx, extension):
        await self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"File `{extension}.py` has been reloaded!")
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

async def setup(bot):
    await bot.add_cog(Reload(bot=bot))