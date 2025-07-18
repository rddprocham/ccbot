import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv
import os

from pydactyl import PterodactylClient

api = PterodactylClient(os.getenv("PTERODACTYL-PANEL"), os.getenv("PTERODACTYL-KEY"))

import os
import json

import asyncio

from urllib.error import HTTPError

from scripts.pnicer import cogs_loaded, error

load_dotenv("settings/.env")

#Load admins
try:
    with open("settings/cadmins.json","r") as e:
        json_cadmins = json.load(e)
        whitelist_admins = json_cadmins["whitelist-admins"]
except FileNotFoundError:
    whitelist_admins = []
    with open("settings/cadmins.json","w") as e:
        json_cadmins = {"whitelist-admins":whitelist_admins}
        json.dump(json_cadmins,e)


with open("emojis.json","r") as f:
     emojis = json.load(f)

DISCORD_SERVER = int(os.getenv("DISCORD_SERVER"))
WHITELIST_CHANNEL = int(os.getenv("WHITELIST_CHANNEL"))
USERNAMES_CHANNEL = int(os.getenv("USERNAMES_CHANNEL"))

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(DISCORD_SERVER)
        if self.guild is None:
            error(f"Guild with ID {DISCORD_SERVER} not found.")
            return
        
        self.whitelist_channel = self.guild.get_channel(WHITELIST_CHANNEL)
        if self.whitelist_channel is None:
            error(f"Whitelist channel with ID {WHITELIST_CHANNEL} not found in guild {DISCORD_SERVER}.")
            return
        
        self.usernames_channel = self.guild.get_channel(USERNAMES_CHANNEL)
        if self.usernames_channel is None:
            error(f"Usernames channel with ID {USERNAMES_CHANNEL} not found in guild {DISCORD_SERVER}.")
            return


    @commands.Cog.listener()
    async def on_message(self, message):
        global cadmins
        global api
        if message.author == self.bot.user:
            return

        if message.channel == self.whitelist_channel:
            if message.content.startswith("#"):
                return
            try:
                # api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist add {message.content}")
                await message.channel.send(f"Simulation: ajout de {message.content} à la whitelist")
            except HTTPError as err:
                if err.code == 412:
                    await message.channel.send(f"`HTTP 412: Le serveur semble être éteint")
                    error("HTTP 412: Le serveur semble être éteint")
                    return
            await message.channel.send(f"`{message.content}` a été ajouté à la whitelist")
            async for msg in self.usernames_channel.history():
                if msg.content == message.content:
                    dm = await msg.author.create_dm()
                    await dm.send(f"Vous avez bien été ajouté à la whitelist du serveur La Terre Oubliée!\n-# Vous n'êtes pas {message.content}? Veuillez signaler ce problème au staff")
            
            await asyncio.sleep(3)
            await message.channel.send(f"`Simulation: whitelist reload")
            # api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist reload")

    async def cog_load(self):
        cogs_loaded("Whitelist")

async def setup(bot):
     with open("settings/settings.json", 'r') as f:
        settings = json.load(f)
        if settings["disable_whitelist"] != True:
            await bot.add_cog(Whitelist(bot=bot))
        else:
            cogs_loaded("Whitelist", False)


