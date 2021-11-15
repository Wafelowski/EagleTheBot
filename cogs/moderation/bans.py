import json
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.role import R

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class Bans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command()
    @has_permissions(ban_members=True)  
    async def ban(ctx, member : discord.Member, *, reason = None):
        await member.ban(reason = reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Nie podano wszystkich argumentów!")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send("Nieznany błąd!")

def setup(bot):
    bot.add_cog(Bans(bot))