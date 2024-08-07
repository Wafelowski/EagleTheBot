import tomli, discord, math, re
from discord.ext import commands
from discord.ext.commands import MemberConverter

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]

class Avatars(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @bot.command()
    async def avatar(self, ctx):
        if len(ctx.message.mentions) == 0:
            content = ctx.message.content.split(" ")
            if len(content) >= 2:
                converter = MemberConverter()
                member = await converter.convert(ctx, content[1])
                if member == None:
                    member = ctx.message.author
            else: 
                member = ctx.message.author
        else:
            member = ctx.message.mentions[0]
            if member is None:
                member = ctx.message.author
                
        embed=discord.Embed(title=f"Avatar - {member.name}", color=member.color, timestamp=ctx.message.created_at, url=member.display_avatar)
        embed.set_image(url=member.display_avatar)
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

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @bot.command()
    async def userinfo(self, ctx):
        if len(ctx.message.mentions) == 0:
            content = ctx.message.content.split(" ")
            if len(content) >= 2:
                converter = MemberConverter()
                member = await converter.convert(ctx, content[1])
                if member == None:
                    member = ctx.message.author
            else: 
                member = ctx.message.author
        else:
            member = ctx.message.mentions[0]
            if member is None:
                member = ctx.message.author

        if member == None:
            member = ctx.message.author

        if member.public_flags == "":
            flagi = "Brak"
        else:
            #flagi = member.public_flags.all()
            flagi = "Work in Progress"
        role = list(map(lambda r: r.id, member.roles))
        role.pop(0)
        role = ["<@&" + str(sub) + ">" for sub in role]
        role2 = ", ".join(role)
        
        embed=discord.Embed(title=f"{member.name}#{member.discriminator}", color=member.color, timestamp=ctx.message.created_at, url=member.display_avatar)
        embed.add_field(name="Użytkownik", value=f"{member.display_name}", inline=True)
        embed.add_field(name="Tag", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="ID", value=f"{member.id}", inline=True)
        embed.add_field(name="Założono", value=f"<t:{await self.convertSnowflakeToDate(member.id)}>", inline=True)
        embed.add_field(name="Flagi", value=f"{flagi}", inline=True)
        embed.add_field(name="Dołączono", value=f"<t:{math.floor(member.joined_at.timestamp())}>", inline=True)
        if len(role2) != 0:
            embed.add_field(name=f"Role - {len(role)}", value=f"{role2}", inline=True)
        embed.set_thumbnail(url=member.display_avatar)
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