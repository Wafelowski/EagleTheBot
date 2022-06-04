from datetime import datetime
import discord, json, re
from discord.ext import commands
from asyncio import sleep

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

with open("configs/themeparkConfig.json", "r") as config:
    data = json.load(config)
    suggestion_channel = data["suggestion_channel"]
    reactions = data["reactions"]

class Reactions(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot
        self.intents = intents

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            if message.channel.id == suggestion_channel:
                for reaction in reactions:
                    if reaction in re.findall(".* .*", reaction):
                        continue
                    elif reaction in re.findall("[0-9]*", reaction):
                        emoji = self.bot.get_emoji(int(reaction))
                    else:
                        emoji = reaction

                    if emoji is None:
                        continue
                    else:
                        await message.add_reaction(emoji)


async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Reactions(bot, intents=intents))