import discord
from discord.ext import commands, tasks
from settings import MINECRAFT_SERVER
from mcstatus import JavaServer

from dotenv import load_dotenv
import os

#Load env variables
load_dotenv()

DISCORD_SERVER = int(os.getenv("DISCORD_SERVER"))
CHANNEL = int(os.getenv("CHANNEL"))

import asyncio
class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_message.start()
        self.msg = None

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(DISCORD_SERVER)
        if guild is None:
            print(f"Guild with ID {DISCORD_SERVER} not found.")
            return
        
        channel = guild.get_channel(CHANNEL)
        if channel is None:
            print(f"Channel with ID {CHANNEL} not found in guild {DISCORD_SERVER}.")
            return
        
        embed = discord.Embed(title="modif")
        try:
             self.msg = await channel.fetch_message(
                  channel.last_message_id)
        except:
            self.msg = await channel.send(embed=embed)
        
        print("Message sent and stored successfully.")



    def cog_unload(self):
        self.send_message.cancel()

    @tasks.loop(seconds=30)
    async def send_message(self):
        await asyncio.sleep(3)
        try:
                    server = JavaServer.lookup(MINECRAFT_SERVER)
                    status = server.status()

                    embed = discord.Embed(title="Statut du serveur")

                    embed.add_field(name="IP",
                                    value=MINECRAFT_SERVER,
                                    inline=False)
                    
                    embed.add_field(name="Statut",
                                    value="En ligne",
                                    inline=False)
                    embed.add_field(name="Ping",
                                    value=f"{round(status.latency)}ms",
                                    inline=False)
                    embed.add_field(name="Nombre de joueurs",
                                    value=f"{status.players.online}",
                                    inline=False)


                # await channel.send(embed=embed)
                    await self.msg.edit(embed=embed)
        except Exception:
                    embed = discord.Embed(title="Statut du serveur")

                    embed.add_field(name="Statut",
                                    value="Hors-ligne",
                                    inline=False)

                    await self.msg.edit(embed=embed)

    @send_message.before_loop
    async def before_send_message(self):
        await self.bot.wait_until_ready()

        
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

async def setup(bot):
    await bot.add_cog(Status(bot=bot))


