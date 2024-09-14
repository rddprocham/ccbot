import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv
import os

from pydactyl import PterodactylClient

api = PterodactylClient(os.getenv("PTERODACTYL-PANEL"), os.getenv("PTERODACTYL-KEY"))

import os
import json

import asyncio


#Load env variables
load_dotenv()

#Load admins
with open("cadmins.json","r") as e:
     json_cadmins = json.load(e)
     cadmins = json_cadmins["cadmins"]
     cloweradmins = json_cadmins["cloweradmins"]
     clowerauth = json_cadmins["clowerauth"]


with open("emojis.json","r") as f:
     emojis = json.load(f)

DISCORD_SERVER = int(os.getenv("DISCORD_SERVER"))
CHANNEL = int(os.getenv("CONSOLE-CHANNEL"))
WHITELIST_CHANNEL = int(os.getenv("WHITELIST_CHANNEL"))
USERNAMES_CHANNEL = int(os.getenv("USERNAMES_CHANNEL"))

class Console(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_console.start()
        self.first_run = True
        self.previous_lines = []
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(DISCORD_SERVER)
        if self.guild is None:
            print(f"Guild with ID {DISCORD_SERVER} not found.")
            return
        
        self.channel = self.guild.get_channel(CHANNEL)
        if self.channel is None:
            print(f"Channel with ID {CHANNEL} not found in guild {DISCORD_SERVER}.")
            return
        
        self.whitelist_channel = self.guild.get_channel(WHITELIST_CHANNEL)
        if self.channel is None:
            print(f"Channel with ID {WHITELIST_CHANNEL} not found in guild {DISCORD_SERVER}.")
            return
        
        self.usernames_channel = self.guild.get_channel(USERNAMES_CHANNEL)
        if self.channel is None:
            print(f"Channel with ID {USERNAMES_CHANNEL} not found in guild {DISCORD_SERVER}.")
            return


    @commands.Cog.listener()
    async def on_message(self, message):
        global cadmins
        global api
        if message.author == self.bot.user:
            return

        if message.channel == self.whitelist_channel:
            api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist add {message.content}")
            await message.channel.send(f"`{message.content}` a été ajouté à la whitelist")
            async for msg in self.usernames_channel.history():
                if msg.content == message.content:
                    dm = await msg.author.create_dm()
                    await dm.send(f"Vous avez bien été ajouté à la whitelist du serveur La Terre Promise!\n-# Vous n'êtes pas {message.content}? Veuillez signaler ce problème au staff")
            
            asyncio.sleep(3)
            api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=f"whitelist reload")

        if message.channel.id!=CHANNEL:
            return
        content = message.content
        if content.startswith("."):
            if message.author.id in cloweradmins:
                command = content[1:]
                if command.startswith(tuple(clowerauth)):
                    await message.channel.send(f"Commande envoyée: `{command}`")
                    api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=command)
            elif message.author.id in cadmins:
                command = content[1:]
                await message.channel.send(f"Commande envoyée: `{command}`")
                api.client.servers.send_console_command(server_id=os.getenv("PTERODACTYL-SERVER"),cmd=command)
            else:
                await message.channel.send(f"Tu n'as pas les permissions pour accéder à la console!)")

    @tasks.loop(seconds=5)
    async def check_console(self):
        global api
        try:
            response = api.client.servers.files.get_file_contents(server_id=os.getenv("PTERODACTYL-SERVER"), path="logs/latest.log")
            res_str = response.text
            res_list = res_str.split('\n')
            if len(res_list)>5:
                res_list.pop()
        except Exception as e:
            print(f"Error fetching file contents: {e}")

        current_lines = [line.strip() for line in res_list] # Read all lines and strip whitespace

        if current_lines != self.previous_lines:
            # Find changed lines
            changed_lines = []
            max_len = max(len(self.previous_lines), len(current_lines))

            for i in range(max_len):
                if i >= len(self.previous_lines) or i >= len(current_lines) or self.previous_lines[i] != current_lines[i]:
                    changed_lines.append((i, current_lines[i] if i < len(current_lines) else ''))

            # Only print the changed lines if this isn't the first run
            if not self.first_run and changed_lines:
                for index, line in changed_lines:
                    await self.channel.send(f"`{line}`")

            self.previous_lines = current_lines
            self.first_run = False  # Set the flag to False after the first run


        

    @check_console.before_loop
    async def before_send_message(self):
        await self.bot.wait_until_ready()
    
    def cog_unload(self):
        self.send_message.cancel()

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

async def setup(bot):
    await bot.add_cog(Console(bot=bot))


