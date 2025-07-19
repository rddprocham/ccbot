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
        json_cadmins = whitelist_admins
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
            return

        username_message = await usernames_channel.fetch_message(reaction.message_id)

        if reaction.member.id not in whitelist_admins:
            await username_message.remove_reaction(reaction.emoji.name, reaction.member)
            return
        if reaction.emoji.name != "✅":
            await username_message.remove_reaction(reaction.emoji.name, reaction.member)
            return
        if username_message.reactions[0].count > 1:
            await username_message.remove_reaction(reaction.emoji.name, reaction.member)
            return

        #Load discord-minecraft usernames
        try:
            with open("discord_minecraft_users.json","r") as e:
                dmusers = json.load(e)
        except FileNotFoundError:
            dmusers = []

        already_exist = False
        for i in range(len(dmusers)):
            if dmusers[i]["dc_usr"] == username_message.author.id:
                dmusers[i]["mc_usr"] = username_message.content
                dmusers[i]["msg_id"] = username_message.id
                dmusers[i]["authorized"] = True
                already_exist = True
                msg = await whitelist_channel.send(f"Simulation: `{username_message.content}`/{f"<@{username_message.author.id}>"} a été ajouté de nouveau validé.")

        if not already_exist:
            dmusers.append({"dc_usr":username_message.author.id,"mc_usr":username_message.content,"msg_id":username_message.id, "authorized":True})
            msg = await whitelist_channel.send(f"Simulation: `{username_message.content}`/{f"<@{username_message.author.id}>"} a été ajouté à la whitelist")
        with open("discord_minecraft_users.json","w") as e:
            json_cadmins = dmusers
            json.dump(json_cadmins,e)

        try:
            await msg.reply(f"Le joueur a correctement été ajouté au serveur <@{reaction.member.id}>")
            # api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist add {username_message.content}")
        except HTTPError as err:
            if err.code == 412:
                await msg.reply(f"`HTTP 412: Le serveur semble être éteint <@{reaction.member.id}>")
                error("HTTP 412: Le serveur semble être éteint")
                return

        # async for msg in usernames_channel.history():
        #     if msg.content == username_message.content:
        #         dm = await msg.author.create_dm()
        #         await dm.send(f"Vous avez bien été ajouté à la whitelist du serveur La Terre Oubliée!\n-# Vous n'êtes pas {username_message.content}? Veuillez signaler ce problème au staff")
        
        await asyncio.sleep(3)
        await whitelist_channel.send(f"Simulation: `whitelist reload`")
        # api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist reload")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        global usernames_channel
        global whitelist_channel

        if reaction.channel_id != USERNAMES_CHANNEL:
            return

        username_message = await usernames_channel.fetch_message(reaction.message_id)

        if username_message.reactions:
            return

        if reaction.emoji.name == "✅":

            try:
                with open("discord_minecraft_users.json","r") as e:
                    dmusers = json.load(e)
            except FileNotFoundError:
                dmusers = []
            
            
            index = 0
            for uid in dmusers:
                if uid["dc_usr"] == username_message.author.id:

                    msg = await whitelist_channel.send(f"Simulation: La validation de `{uid["mc_usr"]}`/{f"<@{uid["dc_usr"]}>"} a été retirée")
                    dmusers[index]["authorized"] = False
                    with open("discord_minecraft_users.json","w") as e:
                        json_cadmins = dmusers
                        json.dump(json_cadmins,e)

                    try:
                        # api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist remove {username_message.content}")
                        await msg.reply(f"Simulation: Ce joueur a été automatiquement retiré de la whitelist")
                    except HTTPError as err:
                        if err.code == 412:
                            await msg.reply(f"HTTP 412: Le serveur semble être éteint: impossible de retirer automatiquement ce joueur de la whitelist")
                            error("HTTP 412: Le serveur semble être éteint")
                            return
        

        await asyncio.sleep(3)
        await whitelist_channel.send(f"Simulation: `whitelist reload`")
        # api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist reload")
    
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        global usernames_channel
        global whitelist_channel

        if payload.channel_id != USERNAMES_CHANNEL:
            return
        
        try:
            with open("discord_minecraft_users.json","r") as e:
                dmusers = json.load(e)
        except FileNotFoundError:
            dmusers = []

        index = 0
        for uid in dmusers:
            if uid["msg_id"] == payload.message_id:
                dmusers[index]["authorized"] = False
                with open("discord_minecraft_users.json","w") as e:
                    json_cadmins = dmusers
                    json.dump(json_cadmins,e)
                
                msg = await whitelist_channel.send(f"Simulation: Le message de `{uid["mc_usr"]}`/{f"<@{uid["dc_usr"]}>"} a été retiré de <#{USERNAMES_CHANNEL}>")

                try:
                    # api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist remove {username_message.content}")
                    await msg.reply(f"Simulation: Ce joueur a été automatiquement retiré de la whitelist")
                except HTTPError as err:
                    if err.code == 412:
                        await msg.reply(f"`HTTP 412: Le serveur semble être éteint: impossible de retirer automatiquement ce joueur de la whitelist")
                        error("HTTP 412: Le serveur semble être éteint")
                        return
                
                await asyncio.sleep(3)
                await whitelist_channel.send(f"Simulation: `whitelist reload`")

                return
            index += 1
        
    async def cog_load(self):
        cogs_loaded("Whitelist")

async def setup(bot):
     with open("settings/settings.json", 'r') as f:
        settings = json.load(f)
        if settings["disable_whitelist"] != True:
            await bot.add_cog(Whitelist(bot=bot))
        else:
            cogs_loaded("Whitelist", False)