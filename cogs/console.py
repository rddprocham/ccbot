import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv
import os

from pydactyl import PterodactylClient

api = PterodactylClient(os.getenv("PTERODACTYL-PANEL"), os.getenv("PTERODACTYL-KEY"))

import os
import json


#Load env variables
load_dotenv()

#Load admins
with open("cadmins.json","r") as e:
     cadmins = json.load(e)

with open("emojis.json","r") as f:
     emojis = json.load(f)

DISCORD_SERVER = int(os.getenv("DISCORD_SERVER"))
CHANNEL = int(os.getenv("CONSOLE-CHANNEL"))

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

    @tasks.loop(seconds=10)
    async def check_console(self):
        global api
        try:
            response = api.client.servers.files.get_file_contents(server_id=os.getenv("PTERODACTYL-SERVER"), path="logs/latest.log")
            res_str = response.text
            res_list = res_str.split('\n')
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
                print(f"Number of changed lines: {len(changed_lines)}")
                for index, line in changed_lines:
                    print(f"Line {index + 1}: {line}")
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


