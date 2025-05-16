from datetime import datetime
import discord, json, os
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from asyncio import sleep

# checkuser
import re

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]
    administrators = data["administrators"]
    moderators = data["moderators"]

class Invision(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    staff = administrators + moderators

    @bot.command()
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(ban_members=True))
    async def checkuser(self, ctx, profile):

        if re.match(r"https?://polishemergencyv\.com/profile/\d+-\w+/", profile):
            profile = profile.split("/")[4] 
        elif re.match(r"\d+", profile):
            profile = profile
        else:
            return await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}checkuser <profil>\n<profil> - link do profilu lub ID użytkownika znajdujące się w linku\n```", mention_author=False)
        
        



    @checkuser.error
    async def checkuser_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}checkuser <profil> <treść>\n<profil> - link do profilu lub ID użytkownika znajdujące się w linku\n```", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.reply(f"Komenda jest na cooldownie! Spróbuj ponownie za {round(error.retry_after, 2)} sekund(y).", mention_author=False)
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Invision(bot, intents=intents))