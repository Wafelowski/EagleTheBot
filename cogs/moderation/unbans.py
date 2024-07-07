import tomli
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions 

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]
    administrators = data["bot"]["roles"]["administrators"]
    moderators = data["bot"]["roles"]["moderators"]

class Unbans(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    staff = administrators + moderators

    @bot.command(aliases=["odbanuj"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(ban_members=True))
    async def unban(self, ctx, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            await ctx.reply("Musisz podać ID użytkownika.", mention_author=False)
            return

        user = self.bot.get_user(user_id)
        if user is None:
            user = await self.bot.fetch_user(user_id)
        print(user)
        await ctx.guild.unban(user)
        
        description = f"""**Odbanowano użytkownika.**\n
        **Użytkownik**: <@{user.id}> ({user.name}#{user.discriminator}) 
        **Administrator**: <@{ctx.author.id}> ({ctx.author.id})"""
        embed2=discord.Embed(description=description, color=0x00ff00, timestamp=ctx.message.created_at)
        embed2.set_author(name=ctx.guild.name)
        embed2.set_footer(text=footer, icon_url=footer_img)
        await ctx.send(embed=embed2)
        await ctx.message.delete()

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Nie podano wszystkich argumentów!")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Unbans(bot, intents=intents))