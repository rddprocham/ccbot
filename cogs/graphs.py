import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import json

load_dotenv()

DISCORD_SERVER = int(os.getenv("DISCORD_SERVER"))
CHANNEL = int(os.getenv("GRAPHS_CHANNEL"))

def graphs(time_str, time_int, time_description, time_unit):
            server = JavaServer.lookup(os.getenv("MINECRAFT_SERVER"))
            status = server.status()

            with open("players_online.json", 'r') as f:
                data = json.load(f)
            
            last_mins = data[time_str]
            if time_str == "60min":
                last_mins.append(status.players.online)
            elif time_str == "1h":
                temp = 0
                for i in range(60):
                    temp += data["60min"][i]
                temp /= 60
                temp = round(temp)
                last_mins.append(temp)
                print(temp)
            data[time_str] = last_mins
            if len(last_mins) > time_int:
                last_mins.pop(0)
            
            with open("players_online.json", "w") as f:
                json.dump(data, f, indent=4)
            
            print(last_mins)

            x = list(range(1, len(last_mins) + 1))
            y = last_mins
            
            plt.plot(x,y)
            plt.xlabel(time_unit)
            plt.ylabel('Joueurs')
            plt.title(f'Joueurs en ligne ces dernières {time_description}')

            plt.ylim(0)

            plt.savefig(f'plot_{time_str}.png')

            plt.clf()



class Graphs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
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
    
        self.graph_message_60s = await channel.send("En cours de création du graphique de 60s...")
        self.graph_message_1h = await channel.send("En cours de création du graphique de 1h...")
        self.min.start()
        self.hour.start()
    

    @tasks.loop(seconds=60)
    async def min(self):
        graphs("60min", 60, "60 minutes", "Minutes")
        if self.graph_message_60s:
            await self.graph_message_60s.delete()
        
        channel = self.bot.get_channel(CHANNEL)
        self.graph_message_60s = await channel.send(file=discord.File('plot_60min.png'))
    
    @tasks.loop(seconds=3600)
    async def hour(self):
        graphs("1h", 24, "24 heures", "Heures")
        if self.graph_message_1h:
            await self.graph_message_1h.delete()
        
        channel = self.bot.get_channel(CHANNEL)
        self.graph_message_1h = await channel.send(file=discord.File('plot_1h.png')) 
         

    

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

async def setup(bot):
    await bot.add_cog(Graphs(bot=bot))