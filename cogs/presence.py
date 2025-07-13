import discord
from discord.ext import commands, tasks
import asyncio

import json

from mcstatus import JavaServer

import os
from dotenv import load_dotenv

from scripts.pnicer import cogs_loaded

load_dotenv("settings/.env")

class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence.start()


    @tasks.loop(seconds=20)
    async def presence(self):
        self.guild = self.bot.get_guild(int(os.getenv("DISCORD_SERVER")))
        self.count = 0
        
        for member in self.guild.members:
            if member.status != discord.Status.offline:
                self.count += 1
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.count} comptes en ligne sur le serveur discord"))

        await asyncio.sleep(10)
        self.server = JavaServer.lookup(os.getenv("MINECRAFT_SERVER"))
        self.status = self.server.status()
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.status.players.online} joueur{'' if self.status.players.online == 1 else 's'} sur le serveur minecraft LTP"))

    @presence.before_loop
    async def before_presence(self):
        await self.bot.wait_until_ready()

    async def cog_load(self):
        cogs_loaded("Presence")

async def setup(bot):
    with open("settings/settings.json", 'r') as f:
        settings = json.load(f)
        if settings["disable_presence"] != True:
            await bot.add_cog(Presence(bot=bot))
        else:
            cogs_loaded("Presence", False)
