import discord
from discord.ext import commands

from scripts.pnicer import cogs_loaded

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['r'])
    async def reload(self, ctx, extension):
        await self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"File `{extension}.py` has been reloaded!")
        cogs_loaded(extension, "r")
    async def cog_load(self):
        cogs_loaded("Reload")

async def setup(bot):
    await bot.add_cog(Reload(bot=bot))