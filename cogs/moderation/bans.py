import json
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

class Bans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command()
    @has_permissions(ban_members=True)  
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        if member.id == ctx.author.id:
            await ctx.send("Dlaczego chcesz zbanować samego siebie?")
            return
        days=0
        daysMsg = ""
        if "-24h" in ctx.message.content:
            days=1
            reason = reason.replace('-24h', '')
            daysMsg = "\nDodatkowo usunięto wiadomości z ostatnich 24 godzin."
        if "-7d" in ctx.message.content:
            days=7
            reason = reason.replace('-7d', '')
            daysMsg = "\nDodatkowo usunięto wiadomości z ostatnich 7 dni."
        silentMsg = "[Flaga -s]"
        if not "-s" in ctx.message.content:
            silentMsg = ""
            description = f"""Otrzymano banicję. Powód: {reason}"""
            embed=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
            embed.set_author(name=ctx.guild.name)
            embed.set_footer(text=footer, icon_url=footer_img)
            await member.send(embed=embed)
        reason = reason.replace('-s', '')
        description = f"""**Nadano banicję.**\n
        **Użytkownik**: <@{member.id}> ({member.name}#{member.discriminator}) 
        **Administrator**: <@{ctx.author.id}> ({ctx.author.id}) 
        **Powód**: {reason} {silentMsg} \n{daysMsg}"""
        embed2=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
        embed2.set_author(name=ctx.guild.name)
        embed2.set_footer(text=footer, icon_url=footer_img)
        try:
            await member.ban(days=days, reason = f"{reason} {silentMsg} {daysMsg}")
        except:
            await ctx.send("Wystąpił błąd. [Bans-53]")
        await ctx.send(embed=embed2)
        

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply("Nie podano wszystkich argumentów!", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send("Nieznany błąd!")

def setup(bot):
    bot.add_cog(Bans(bot))