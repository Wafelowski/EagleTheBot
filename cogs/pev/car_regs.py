from datetime import datetime
import discord, json, os
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from asyncio import sleep

# Rejestracja
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

class CarRegistrations(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @bot.command()
    @commands.cooldown(1, 30, commands.BucketType.user) 
    async def rejestracja(self, ctx, reg_prefix, reg_suffix):
        if (len(reg_prefix) != 3) or (len(reg_suffix) > 4):
            return await ctx.reply("Komenda nie wspiera na ten moment innego formatu niż XXX X???. Gdzie X to wymagany znak, a ? to dowolny znak.", mention_author=False)


        img = Image.open('db/pev/rejestracja.png')
        img_process = ImageDraw.Draw(img)

        # Znaczek PL i flaga UE
        plFont = ImageFont.truetype('db/pev/arklatrs.ttf', 240)

        # Tekst
        font = ImageFont.truetype('db/pev/arklatrs.ttf', 260)

        text = []

        temp = reg_prefix.lower().strip("")
        for x in temp:
            text.append(x)

        temp = reg_suffix.upper().strip("")
        for x in temp:
            text.append(x)

        # Pierwsze 2/3 litery - ZWĘŻONE CZYLI MAŁE
        # POZOSTAŁE - DUŻE

        coordinates_triple = [
            129,
            285,
            442,
            652,
            809,
            966,
            1122
        ]

        coordinates_double = [] #TODO: Fill this

        # Flaga + PL
        img_process.text((22, 16), "*", font=plFont, fill=(255, 255, 0))
        img_process.text((112, 34), "|", font=plFont, fill=(255, 255, 255))

        # Tekst
        for i, letter in enumerate(text):
            if len(reg_prefix) == 3:
                img_process.text((coordinates_triple[i], 6), letter, font=font, fill=(0, 0, 0))
            elif len(reg_prefix) == 2:
                return

        img.save(f'db/temp/{ctx.author.id}.png', "PNG")

        img = discord.File(f'db/temp/{ctx.author.id}.png', filename=f'{ctx.author.id}.png', spoiler=False)

        await ctx.reply(
            content = f"Rejestracja `{reg_prefix.upper()} {reg_suffix.upper()}` wygenerowana pomyślnie!",
            file = img,
            mention_author = False
        )

    @rejestracja.error
    async def patreon_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}rejestracja <przedrostek> <treść>\n```", mention_author=False)
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
    await bot.add_cog(CarRegistrations(bot, intents=intents))