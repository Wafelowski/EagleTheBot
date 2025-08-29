import discord, tomli
from discord.ext import commands
from pev_db import execute_query, get_connection

# checkuser
import re

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]
    administrators = data["bot"]["roles"]["administrators"]
    moderators = data["bot"]["roles"]["moderators"]

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
        
        print(profile)

        # from profile get id, for example "2-wafel"

        DB = get_connection()


        # 

        async with DB.cursor() as cursor:
            await cursor.execute("SELECT * FROM users WHERE profile_id = %s", (profile,))
            result = await cursor.fetchone()
            if result:
                await ctx.reply(f"Znaleziono użytkownika: {result['username']}", mention_author=False)
            else:
                await ctx.reply("Nie znaleziono użytkownika.", mention_author=False)

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