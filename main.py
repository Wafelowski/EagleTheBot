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
class EagleBot(commands.Bot):
    async def setup_hook(self):
        print(f"""Zalogowano jako {self.user}
Discord.py - {discord.__version__}
Bot by Wafelowski.dev""")
        if status_list != False:
            status_change.start()
        # await self.load_extension(...)

bot = EagleBot(command_prefix=commands.when_mentioned_or(prefix), intents=intents, help_command=None)

# Load cogs
async def load_cogs_category(bot, category, category_name=None):
    """
    Loads all the Python files ending with '.py' in the specified category directory as extensions for the bot.

    Args:
        bot (discord.ext.commands.Bot): The bot instance.
        category (str): The name of the category directory containing the cogs.
        category_name (str, optional): The display name of the category. Defaults to None.

    Returns:
        None
    """
    if category_name is None:
        category_name = category

    for filename in os.listdir(f"cogs/{category}"):
        if filename.endswith(".py"):
            cog_path = f"cogs.{category}.{filename[:-3]}"
            await bot.load_extension(cog_path)
            print(f"[Cogs - {category_name}] Loaded - {filename[:-3]}")

async def load_all_cogs(bot, modules_mapping):
    """
    Load all cogs based on the given modules_mapping.

    Parameters:
    - bot (discord.ext.commands.Bot): The bot instance.
    - modules_mapping (dict): A dictionary mapping modules to categories.

    Returns:
    - None
    """
    for module, category in modules_mapping.items():
        if module is None:
            # Handle files in the root directory
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    cog_path = f"cogs.{filename[:-3]}"
                    await bot.load_extension(cog_path)
                    print(f"[Cogs] Loaded - {filename[:-3]}")
        elif os.path.exists(f"cogs/{category}"):
            await load_cogs_category(bot, category, module)

if __name__ == '__main__':
    pev_module = os.path.exists("cogs/pev")
    themepark_module = os.path.exists("cogs/themepark")

    modules_mapping = {
        None: "",  # For cogs at the root level
        "Moderation": "moderation",
        "Utilities": "util",
        "Fun": "fun",
        "PolishEmergencyV": "pev" if pev_module else None,
        "ThemePark": "themepark" if themepark_module else None,
    }

    asyncio.run(load_all_cogs(bot, modules_mapping))

@loop()
async def status_change():
    """
    A coroutine function that changes the bot's status periodically.

    This function iterates over a list of statuses and updates the bot's presence
    with each status. It uses the `discord.Activity` class to set the activity type
    and name of the status. The function then waits for a specified duration before
    moving on to the next status.

    Note: This function should be used as a decorator for an asynchronous event loop.

    Args:
        None

    Returns:
        None
    """
    for status in status_list:
        statusType = eval(f"discord.ActivityType.{status[0]}")
        await bot.change_presence(activity=discord.Activity(type=statusType, name=status[1]))
        await sleep(int(status[2]))

@status_change.before_loop
async def before_loop_func():
    """
    This function is called before the status_change loop starts.
    It waits for the bot to be ready before proceeding.
    """
    await bot.wait_until_ready()

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

async def sendError(error, err_type = "Error"):
    if err_type == "Error":
        logger.error(error)
    elif err_type == "Warning":
        logger.warning(error)
    elif err_type == "Info":
        logger.info(error)
    elif err_type == "Debug":
        logger.debug(error)
    else:
        logger.error(error)

    channel = bot.get_channel(error_channel)
    if channel is None:
        raise error

    embed = discord.Embed(title=f"**{err_type}**", description=f"```{error}```", color=0xff0000)
    embed.set_footer(text=footer, icon_url=footer_img)
    await channel.send(embed=embed)
    return embed
cleanupTemp()

bot.run(token)