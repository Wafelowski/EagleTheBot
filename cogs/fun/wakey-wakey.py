from datetime import datetime
import discord, tomli
from discord.ext import commands
from asyncio import sleep

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    administrators = data["bot"]["roles"]["administrators"]
    moderators = data["bot"]["roles"]["moderators"]

class Pobudka(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    staff = administrators + moderators

    @bot.command(aliases=["wakey-wakey", "wakeup", "wake-up"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(administrator=True))
    async def pobudka(self, ctx, user):
        if ctx.message.mention_everyone:
            await ctx.reply("Na co liczysz?", mention_author=False, delete_after=15.0)
            return
        
        if len(ctx.message.mentions) > 1:
            await ctx.reply("Możesz podać tylko jednego użytkownika.", mention_author=False, delete_after=15.0)
            return
        elif len(ctx.message.mentions) == 0:
            member = ctx.guild.get_member(user)
            if member is None:
                await ctx.reply("Nie znaleziono użytkownika.", mention_author=False, delete_after=15.0)
                return
        else:
            member = ctx.message.mentions[0]

        for i in range(1, 10):
            await ctx.send(f"Pobudka {member.mention}!")
            if i == 4 or i == 8:
                await sleep(2) 

    @pobudka.error
    async def pobudka_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}pobudka <ID/@Użytkownik>\n```", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.CheckAnyFailure):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")
            raise error

    @bot.command(aliases=[])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(administrator=True))
    async def zebranie(self, ctx, role):
        if ctx.message.mention_everyone:
            await ctx.reply("Na co liczysz?", mention_author=False, delete_after=15.0)
            return

        if len(ctx.message.role_mentions) > 1:
            await ctx.reply("Możesz podać tylko jedną rolę.", mention_author=False, delete_after=15.0)
            return
        elif len(ctx.message.role_mentions) == 0:
            role = ctx.guild.get_role(role)
            if role is None:
                await ctx.reply("Nie znaleziono roli.", mention_author=False, delete_after=15.0)
                return
        else:
            role = ctx.message.role_mentions[0]

        for i in range(1, 10):
            await ctx.send(f"Zebranie {role.mention}!")
            if i == 4 or i == 8:
                await sleep(2)

    @zebranie.error
    async def zebranie_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}zebranie <ID/@Rola>\n```", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.CheckAnyFailure):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")
            raise error

async def setup(bot):
    pass
    # intents = discord.Intents.default()
    # intents.members = True
    # await bot.add_cog(Pobudka(bot, intents=intents))