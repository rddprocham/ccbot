import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

import json

load_dotenv()


class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, what):
        await ctx.send(what)
        await ctx.message.delete()

    @commands.command()
    async def open_dm(self, ctx, user_id):
        user = await self.bot.fetch_user(user_id)
        guild = ctx.message.guild
        channel = await guild.create_text_channel(name=user.name, category=self.bot.get_channel(int(os.getenv("DMS_CATEGORY"))))
        try:
            with open("dms.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        data[user.id] = channel.id
        data[channel.id] = user.id
        with open("dms.json", "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"Salon privé créé!")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        guild = message.guild
        category = self.bot.get_channel(int(os.getenv("DMS_CATEGORY")))
        if message.guild and message.channel.category != category:
            return
        try: 
            with open("dms.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        #If the message is sent from the server
        if message.guild and message.channel.category == category:
            user = discord.utils.get(guild.members, id=data[str(message.channel.id)])
            dm = await user.create_dm()
            if message.content and message.content.startswith("_") == False:
                await dm.send(message.content)
            if message.attachments:
                for attachment in message.attachments:
                    await dm.send(attachment.url)
        #If the message is sent from the DM
        if message.guild == None:
            #If a channel is already created 
            if str(message.author.id) in data.keys():  
                channel_to_send = self.bot.get_channel(data[str((message.author.id))])
            else:
            #If a channel is not created
                guild = self.bot.get_guild(int(os.getenv("DISCORD_SERVER_ID")))
                channel = await guild.create_text_channel(name=message.author.name, category=self.bot.get_channel(int(os.getenv("DMS_CATEGORY"))))
                data[message.author.id] = channel.id
                data[channel.id] = message.author.id
                with open("dms.json", "w") as f:
                    json.dump(data, f, indent=4)
                channel_to_send = self.bot.get_channel(data[str((message.author.id))])
            if message.content:
                await channel_to_send.send(message.content)
            if message.attachments:
                for attachment in message.attachments:
                    await channel_to_send.send(attachment.url)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

async def setup(bot):
    await bot.add_cog(Announcements(bot=bot))
