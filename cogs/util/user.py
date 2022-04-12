import json
import discord
import math
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions 

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

class Avatars(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @bot.command()
    async def avatar(self, ctx):
        if len(ctx.message.mentions) == 0:
            member = ctx.message.author
        else:
            member = ctx.message.mentions[0]
        embed=discord.Embed(title=f"Avatar - {member.name}", color=member.color, timestamp=ctx.message.created_at, url=member.avatar.url)
        embed.set_image(url=member.avatar.url)
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Nie podano wszystkich argumentów!")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send("Nieznany błąd!")

class Userinfo(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @bot.command()
    async def userinfo(self, ctx):
        if len(ctx.message.mentions) == 0:
            member = ctx.message.author
        else:
            member = ctx.message.mentions[0]
        if member.public_flags == "":
            flagi = "Brak"
        else:
            #flagi = member.public_flags
            flagi = "Work in Progress"
        role = list(map(lambda r: r.id, member.roles))
        role.pop(0)
        role = ["<@&" + str(sub) + ">" for sub in role]
        role2 = ", ".join(role)
        embed=discord.Embed(title=f"{member.name}#{member.discriminator}", color=member.color, timestamp=ctx.message.created_at, url=member.avatar.url)
        embed.add_field(name="Użytkownik", value=f"{member.display_name}", inline=True)
        embed.add_field(name="Tag", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="ID", value=f"{member.id}", inline=True)
        embed.add_field(name="Założono", value=f"<t:{await self.convertSnowflakeToDate(member.id)}>", inline=True)
        embed.add_field(name="Flagi", value=f"{flagi}", inline=True)
        embed.add_field(name="Dołączono", value=f"<t:{math.floor(member.joined_at.timestamp())}>", inline=True)
        embed.add_field(name=f"Role - {len(role)}", value=f"{role2}", inline=True)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Nie podano wszystkich argumentów!")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

    async def convertSnowflakeToDate(self, snowflake):
        DISCORD_EPOCH = 1420070400000
        #return new Date(snowflake / 4194304 + epoch)
        return math.floor((snowflake / 4194304 + DISCORD_EPOCH) / 1000)
        

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Avatars(bot, intents=intents))
    await bot.add_cog(Userinfo(bot, intents=intents))