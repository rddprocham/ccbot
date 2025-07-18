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
        global usernames_channel
        global whitelist_channel
        self.guild = self.bot.get_guild(DISCORD_SERVER)
        if self.guild is None:
            error(f"Guild with ID {DISCORD_SERVER} not found.")
            return
        
        whitelist_channel = self.guild.get_channel(WHITELIST_CHANNEL)
        if whitelist_channel is None:
            error(f"Whitelist channel with ID {WHITELIST_CHANNEL} not found in guild {DISCORD_SERVER}.")
            return
        
        usernames_channel = self.guild.get_channel(USERNAMES_CHANNEL)
        if usernames_channel is None:
            error(f"Usernames channel with ID {USERNAMES_CHANNEL} not found in guild {DISCORD_SERVER}.")
            return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        global usernames_channel
        global whitelist_channel
        if reaction.channel_id != USERNAMES_CHANNEL:
            print("failed at check channel")
            return
        if reaction.member.id not in whitelist_admins:
            print("failed at check author")
            return
        if reaction.emoji.name != "✅":
            print("failed at check name")
            return
        print("correct reaction")
        print(reaction)
        username = await usernames_channel.fetch_message(reaction.message_id)
        try:
            print("add to console simulation")
            # api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist add {username.content}")
        except HTTPError as err:
            if err.code == 412:
                await whitelist_channel.send(f"`HTTP 412: Le serveur semble être éteint <@{reaction.member.id}>")
                error("HTTP 412: Le serveur semble être éteint")
                return
        await whitelist_channel.send(f"Simulation: `{username.content}`/{f"<@{username.author.id}>"} a été ajouté à la whitelist")
        async for msg in usernames_channel.history():
            if msg.content == username.content:
                dm = await msg.author.create_dm()
                await dm.send(f"Vous avez bien été ajouté à la whitelist du serveur La Terre Oubliée!\n-# Vous n'êtes pas {username.content}? Veuillez signaler ce problème au staff")
        
        await asyncio.sleep(3)
        await whitelist_channel.send(f"Simulation: `whitelist reload`")
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