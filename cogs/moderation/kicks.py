import json
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions 

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

class Kicks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command()
    @has_permissions(kick_members=True)  
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        if member.id == ctx.author.id:
            await ctx.send("Dlaczego chcesz wyrzucić samego siebie?")
            return
        silentMsg = "[Flaga -s]"
        if not "-s" in ctx.message.content:
            silentMsg = ""
            description = f"""Otrzymano kopa w dupe. Powód: {reason}"""
            embed=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
            embed.set_author(name=ctx.guild.name)
            embed.set_footer(text=footer, icon_url=footer_img)
            await member.send(embed=embed)
        reason = reason.replace('-s', '')
        description = f"""**Wyrzucono użytkownika.**\n
        **Użytkownik**: <@{member.id}> ({member.name}#{member.discriminator}) 
        **Administrator**: <@{ctx.author.id}> ({ctx.author.id}) 
        **Powód**: {reason} {silentMsg}"""
        embed2=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
        embed2.set_author(name=ctx.guild.name)
        embed2.set_footer(text=footer, icon_url=footer_img)
        try:
            await member.kick(reason = f"{reason} {silentMsg}")
        except:
            await ctx.send("Wystąpił błąd. [Kicks-44]")
        await ctx.send(embed=embed2)

    @kick.error
    async def kick_error(self, ctx, error):
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
    bot.add_cog(Kicks(bot))