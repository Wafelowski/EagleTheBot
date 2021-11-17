import json
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=["wyczysc", "wyczyść", "cleanup"])
    @has_permissions(manage_messages=True)  
    async def purge(self, ctx, arg1):
        if isinstance(arg1, int):
            await ctx.send(f"Musisz podać liczbę wiadomości do usunięcia!")
            return
        tooMuchMsg = ""
        number = int(arg1)
        if number >= 100:
            tooMuchMsg = f"**Nie możesz usunąć więcej niż 100 wiadomości!** \nUżyj komendy jeszcze raz jeśli potrzebujesz."
            number = 99
        deleted = await ctx.channel.purge(limit=int(number+1))
        description = f"""Usunięto `{len(deleted)}` wiadomości na `{arg1}` wybranych. \n{tooMuchMsg}"""
        embed=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.guild.name)
        embed.set_footer(text="Wiadomość zniknie za 10 sekund", icon_url=footer_img)
        await ctx.send(embed=embed, delete_after=10)
        

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply("Nie podano wszystkich argumentów!", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

def setup(bot):
    bot.add_cog(Purge(bot))