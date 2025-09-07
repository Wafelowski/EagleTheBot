import tomli
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]
    administrators = data["bot"]["roles"]["administrators"]
    moderators = data["bot"]["roles"]["moderators"]

class Purge(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    staff = administrators + moderators

    @bot.command(aliases=["wyczyść", "wyczyśc", "wyczysć", "wyczysc"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(manage_messages=True))
    @has_permissions(manage_messages=True)  
    async def purge(self, ctx, arg1):
        try:
            number = int(arg1)
        except ValueError:
            await ctx.send(f"Musisz podać liczbę wiadomości do usunięcia!")
            return
        tooMuchMsg = ""
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

    @bot.command()
    @commands.dm_only()
    async def purgeown(self, ctx, arg1):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(f"Ta komenda może być używana tylko w DM!")
            return
        try:
            number = int(arg1)
        except ValueError:
            await ctx.send(f"Musisz podać liczbę wiadomości do usunięcia!")
            return
        tooMuchMsg = ""
        if number >= 100:
            tooMuchMsg = f"**Nie możesz usunąć więcej niż 100 wiadomości!** \nUżyj komendy jeszcze raz jeśli potrzebujesz."
            number = 99
        # Collect last 'number' bot messages in DM by looping in batches of 100
        bot_messages = []
        last_message = None
        while len(bot_messages) < number:
            limit = 100
            async for msg in ctx.channel.history(limit=limit, before=last_message):
                if msg.author == ctx.me:
                    bot_messages.append(msg)
                    if len(bot_messages) >= number:
                        break
                last_message = msg
                # If no more messages, break
                if last_message is None:
                    break
        deleted = []
        for msg in bot_messages[:number]:
            try:
                await msg.delete()
                deleted.append(msg)
            except Exception:
                pass
        description = f"""Usunięto `{len(deleted)}` wiadomości Bota na `{arg1}` wybranych. \n{tooMuchMsg}"""
        embed = discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.me.name)
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
        elif isinstance(error, commands.errors.PrivateMessageOnly):
            await ctx.reply("Ta komenda może być używana tylko w DM!", mention_author=False)
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Purge(bot, intents=intents))