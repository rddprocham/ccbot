import discord
from discord.ext import commands

from scripts.pnicer import cogs_loaded

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        last_cmd = ""

    @commands.command(aliases = ['re'])
    async def reload(self, ctx, extension):
        global last_cmd
        await self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"File `{extension}.py` has been reloaded!")
        cogs_loaded(extension, "r")
        last_cmd = extension
        
    @commands.command(aliases = ["r"])
    async def rereload(self, ctx):
        global last_cmd
        await self.bot.reload_extension(f"cogs.{last_cmd}")
        await ctx.send(f"File `{last_cmd}.py` has been reloaded!")
        cogs_loaded(last_cmd, "r")


    async def cog_load(self):
        cogs_loaded("Reload")

async def setup(bot):
    await bot.add_cog(Reload(bot=bot))