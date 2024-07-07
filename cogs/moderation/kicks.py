import tomli
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions 
from discord.ext.commands import MemberConverter

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]
    administrators = data["bot"]["roles"]["administrators"]
    moderators = data["bot"]["roles"]["moderators"]

class Kicks(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    staff = administrators + moderators

    @bot.command(aliases=["wyrzuc", "wyrzuć"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(kick_members=True))
    async def kick(self, ctx, member, *, reason = None):
        if ctx.message.mention_everyone:
            await ctx.reply("Na co liczysz?", mention_author=False, delete_after=15.0)
            return
        
        if len(ctx.message.mentions) > 1:
            await ctx.reply("Możesz podać tylko jednego użytkownika.", mention_author=False, delete_after=15.0)
            return
        elif len(ctx.message.mentions) == 0:
            converter = MemberConverter()
            member = await converter.convert(ctx, member)
            if member is None:
                await ctx.reply("Nie znaleziono użytkownika.", mention_author=False, delete_after=15.0)
                return
        else:
            member = ctx.message.mentions[0]
        
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
            try:
                await member.send(embed=embed)
            except:
                pass

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
        except Exception as e:
            await ctx.send(f"Wystąpił błąd. [Kicks-64]  ```\n{e}\n```")
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

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Kicks(bot, intents=intents))