from datetime import datetime
import discord, json, re, tomli
from discord.ext import commands
from asyncio import sleep

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]
    active = data["modules"]["fun"]["auto_react"]
    auto_reactions = data["modules"]["fun"]["auto_reactions"]

class Reactions(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot
        self.intents = intents

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    # Convert keys from string to int (TOML keys are strings by default)
    auto_reactions = {int(k): v for k, v in auto_reactions.items()}

    @commands.Cog.listener()
    async def on_message(self, message):
        if not active:
            return
        if message.author.id == self.bot.user.id:
            return  # Ignore bot's own messages
        
        reactions = auto_reactions.get(str(message.channel.id))

        if not reactions:
            return

        for reaction in reactions:
            emoji = None

            # 1️⃣ If custom emoji in format <:name:id>
            match = re.match(r"<a?:\w+:(\d+)>", reaction)
            if match:
                emoji = self.bot.get_emoji(int(match.group(1)))

            # 2️⃣ If numeric emoji ID
            elif reaction.isdigit():
                emoji = self.bot.get_emoji(int(reaction))

            # 3️⃣ Otherwise, treat as Unicode emoji
            else:
                emoji = reaction

            if emoji:
                try:
                    await message.add_reaction(emoji)
                except Exception:
                    pass



async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    if auto_reactions and active:
        await bot.add_cog(Reactions(bot, intents=intents))