import json
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions 

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class Kicks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command()
    @has_permissions(kick_members=True)  
    async def kick(ctx, member : discord.Member, *, reason = None):
        await member.kick(reason = reason)

    @kick.error
    async def kick_error(self, ctx, error):
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
    bot.add_cog(Kicks(bot))