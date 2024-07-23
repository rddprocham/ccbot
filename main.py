import discord
from discord.ext import commands

import os

from dotenv import load_dotenv

#Load env variables
load_dotenv()

class StatusBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=discord.Intents().all())

    async def setup_hook(self):
        await self.load_extension(f'cogs.status')

    async def on_ready(self):
        print("Bot is ready")

StatusBot().run(os.getenv("DISCORD-BOT-TOKEN"))