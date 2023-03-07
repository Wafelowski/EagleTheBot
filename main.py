import os
import discord
import time
import json
import logging
import asyncio
from discord.ext import commands
from discord.ext.tasks import loop
from asyncio import sleep
from datetime import datetime


# Get configuration.json
with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    token = data["token"]
    owner_id = data["ownerID"]
    error_channel = data["errorChannel"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

    status_list = data["statusList"]
    pev_module = data["pevModule"]
    themepark_module = data["themeparkModule"]

if token == "TOKEN":
    print("Błędny token.")
    exit()

def __init__(self, bot):
    self.bot = bot
    self._last_member = None
    self.intents = discord.Intents.default()
    self.intents.members = True

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# The bot
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents, help_command=None)

# Load cogs
async def LoadCogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"[Cogs] Loaded - {filename[:-3]}")

    for filename in os.listdir("cogs/moderation"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.moderation.{filename[:-3]}")
            print(f"[Cogs - Moderation] Loaded - {filename[:-3]}")

    for filename in os.listdir("cogs/util"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.util.{filename[:-3]}")
            print(f"[Cogs - Utilities] Loaded - {filename[:-3]}")

    for filename in os.listdir("cogs/fun"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.fun.{filename[:-3]}")
            print(f"[Cogs - Fun] Loaded - {filename[:-3]}")
    
    if pev_module:
        for filename in os.listdir("cogs/pev"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.pev.{filename[:-3]}")
                print(f"[Cogs - PolishEmergencyV] Loaded - {filename[:-3]}")

    if themepark_module:
        for filename in os.listdir("cogs/themepark"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.themepark.{filename[:-3]}")
                print(f"[Cogs - ThemePark] Loaded - {filename[:-3]}")

if __name__ == '__main__':
    asyncio.run(LoadCogs())


@loop()
async def status_change():
    for status in status_list:
        statusType = eval(f"discord.ActivityType.{status[0]}")
        await bot.change_presence(activity=discord.Activity(type=statusType, name=status[1]))
        await sleep(int(status[2]))
    

@bot.event
async def on_ready():
    print(f"""Zalogowano jako {bot.user}
Discord.py - {discord.__version__}
Bot by Wafelowski.dev""")
    if status_list != False:
            status_change.start()


@bot.listen('on_message')
async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content == "<@754727115710267414>":
            await message.reply(f"Hej {message.author.mention}, mój prefiks to `{prefix}`.")
        if message.content.startswith(f"{prefix}off"):
                await message.channel.send("Okej")
                exit()
        if message.content.startswith(f"{prefix}ping"):
                before = time.monotonic()
                msg = await message.channel.send("🏓 Pong !")
                ping = (time.monotonic() - before) * 1000
                await msg.edit(content=f"🏓 Pong !  `{int(ping)} ms`")
        if message.content.startswith(f"{prefix}setup") and str(message.author.id) == str(owner_id):
            print("Hell nah")
        
        
#@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Witaj {member.mention}.'.format(member))

#@bot.event
async def on_reaction_add(reaction, user):
    channel = bot.get_channel(596428386100838400)
    await channel.send(f'Reakcja - {reaction}. User - {user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound) or isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.CommandOnCooldown):
        return
    print(f"------- \nWystąpił błąd \n--- \n{error} \n-------")
    channel = bot.get_channel(error_channel)
    if channel is None:
        raise error
    await channel.send(f"```{ctx}``` \n\n```{error}```") 
    raise error

#Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Cleanup temp files
def cleanupTemp():
    for filename in os.listdir("db/temp"):
        os.remove(f"db/temp/{filename}")
        logger.debug(f"[Temp] Deleted - {filename}")
cleanupTemp()

async def main():
    async with bot:
        await bot.start(token)

asyncio.run(main())
# bot.run(token)