from datetime import datetime
import discord, tomli, re
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from asyncio import sleep

# Rejestracja
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]

class CarRegistrations(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents = intents)

    def check_word_pattern(word):
        patterns = [
            [1, r'^[a-zA-Z0-9_.-]{3}[a-zA-Z0-9_.-]{1,4}$'],       # 3L 1L_3C
            # [2, r'^[A-Za-z]{3}\d{2}[A-Za-z]{2}$'],    # 3L 2C_2L
            # [3, r'^[A-Za-z]{3}\d[A-Za-z]{2}\d$'],     # 3L 1C_2L_1C
            # [4, r'^[A-Za-z]{3}\d{2}[A-Za-z]\d$'],     # 3L 2C_1L_1C
            [5, r'^[A-Za-z]{2}\d{4}[A-Za-z]$'],       # 2L 4C_1L
            # [6, r'^[A-Za-z]{2}\d{5}$'],               # 2L 5C
        ]

        for pattern in patterns:
            if re.match(pattern[1], word):
                return pattern[1]
        return False

    @bot.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rejestracja(self, ctx, reg_prefix, reg_suffix):
        pattern = CarRegistrations.check_word_pattern(f"{reg_prefix} {reg_suffix}")
        if pattern == 0 or pattern == False:
            return await ctx.reply("Nieprawidłowy format rejestracji! Dostępne formaty to: \n> - XX X??? \n> - XXX X???? \nGdzie X oznacza wymagany znak, a ? opcjonalny.", mention_author=False)
    
        # img = Image.open('cogs/pev/car_regs/rejestracja.png') # DISABLED, no point in using it
        if pattern == 1:
            img = Image.open('cogs/pev/car_regs/rejestracja-3L-1L3C.png')
        elif pattern == 5:
            img = Image.open('cogs/pev/car_regs/rejestracja-2L-4C1L.png')
        img_process = ImageDraw.Draw(img)

        # Znaczek PL i flaga UE
        plFont = ImageFont.truetype('cogs/pev/car_regs/arklatrs.ttf', 240)

        # Tekst
        font = ImageFont.truetype('cogs/pev/car_regs/arklatrs.ttf', 260)

        text = []

        temp = reg_prefix.lower().strip("")
        for x in temp:
            text.append(x)

        temp = reg_suffix.lower().strip("")
        for x in temp:
            text.append(x)

        # Pierwsze 2/3 litery - DUŻE
        # POZOSTAŁE - ZWĘŻONE CZYLI MAŁE

        coordinates_triple = [
            162,
            314,
            466,
            694,
            848,
            1002,
            1156
        ]

        coordinates_double = [
            162,
            319,
            547,
            701,
            855,
            1009,
            1163
        ] #TODO: Fill this

        # Flaga + PL
        img_process.text((22, 16), "*", font=plFont, fill=(255, 255, 0))
        img_process.text((112, 34), "|", font=plFont, fill=(255, 255, 255))

        # Tekst
        for i, letter in enumerate(text):
            if len(reg_prefix) == 3:
                img_process.text((coordinates_triple[i], 6), letter, font=font, fill=(0, 0, 0))
            elif len(reg_prefix) == 2:
                img_process.text((coordinates_double[i], 6), letter, font=font, fill=(0, 0, 0))

        img.save(f'db/temp/{ctx.author.id}.png', "PNG")

        img = discord.File(f'db/temp/{ctx.author.id}.png', filename=f'{ctx.author.id}.png', spoiler=False)

        await ctx.reply(
            content = f"Rejestracja `{reg_prefix.upper()} {reg_suffix.upper()}` wygenerowana pomyślnie!",
            file = img,
            mention_author = False
        )

    @rejestracja.error
    async def rejestracja_error(self, ctx, error):
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