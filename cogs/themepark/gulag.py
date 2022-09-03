from datetime import datetime
from multiprocessing.sharedctypes import Value
import discord, json, os.path
from discord.ext import commands
from asyncio import sleep

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]
    administrators = data["administrators"]
    moderators = data["moderators"]

with open("configs/themeparkConfig.json", "r") as config:
    data = json.load(config)
    gulag_role = data["gulag_role"]
    gulag_staff = data["gulag_staff"]
    gulag_welcome_channel = data["gulag_welcome_channel"]
    gulag_welcome_message = data["gulag_welcome_message"]
    gulag_logs = data["gulag_logs"]

class Gulag(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    staff = gulag_staff + administrators + moderators

    @bot.command(aliases=["gułag", "glg", "głg"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(administrator=True))
    async def gulag(self, ctx, user, number):
        if ctx.message.mention_everyone:
            await ctx.reply("Na co liczysz?", mention_author=False, delete_after=15.0)
            return        

        if len(ctx.message.mentions) > 1:
            await ctx.reply("Możesz podać tylko jednego użytkownika.", mention_author=False, delete_after=15.0)
            return
        elif len(ctx.message.mentions) == 0:
            try:
                user = int(user)
            except ValueError as e:
                await ctx.reply("Podane ID nie jest poprawne.", mention_author=False, delete_after=15.0)
                return

            member = ctx.guild.get_member(user)
            if member is None:
                await ctx.reply("Nie znaleziono użytkownika.", mention_author=False, delete_after=15.0)
                return
        else:
            member = ctx.message.mentions[0]

        try:
            number = int(number)
        except ValueError:
            await ctx.reply("Nieprawidłowa liczba", mention_author=False, delete_after=15.0)
            return

        
        bot_member = ctx.guild.get_member(self.bot.user.id)
        if bot_member.top_role.position < member.top_role.position:
            await ctx.reply("Użytkownik posiada wyższą rolę niz bot.", mention_author=False, delete_after=15.0)
            return
        if ctx.author.id != ctx.guild.owner_id and member.top_role.position >= ctx.author.top_role.position:
            await ctx.reply("Nie możesz wysłać tego użytkownika do gułagu. Jest on wyższy rangą od Ciebie.", mention_author=False, delete_after=15.0)
            return

        welcome_channel = ctx.guild.get_channel(gulag_welcome_channel)
        if welcome_channel is None:
            await ctx.reply(f"Błąd w konfiguracji, nie znaleziono kanału powitań o ID {gulag_welcome_channel}.", mention_author=False, delete_after=15.0)
            return
        logs_channel = ctx.guild.get_channel(gulag_logs)
        if logs_channel is None:
            await ctx.reply(f"Błąd w konfiguracji, nie znaleziono kanału do logów o ID {gulag_logs}.", mention_author=False, delete_after=15.0)
            return

        glg_role = ctx.guild.get_role(gulag_role)
        if glg_role == None:
            await ctx.reply(f"Błąd w konfiguracji, nie znaleziono gułag roli o ID {gulag_welcome_channel}.", mention_author=False, delete_after=15.0)
            return
        if glg_role in member.roles:
            await ctx.reply("Ten użytkownik jest już w gułagu.", mention_author=False, delete_after=15.0)
            return

        roles_id = []
        roles = []
        for role in member.roles:
            if role.permissions.administrator:
                await ctx.reply("Nie możesz wysłać tego użytkownika do gułagu. Jest on administratorem.", mention_author=False, delete_after=15.0)
                return
            if role in gulag_staff:
                await ctx.reply("Nie możesz wysłać służby do gułagu.", mention_author=False, delete_after=15.0)
                return
            if role.name == "@everyone":
                pass
            if role.is_integration():
                pass
            if role.is_premium_subscriber():
                pass
            if role.is_bot_managed():
                pass
            if not role.is_assignable():
                pass
            else:
                roles_id.append(role.id)
                roles.append(role)

        if not os.path.exists(f"db/gulag/{member.id}.json"):
            with open(f"db/gulag/{member.id}.json", "w+") as file:
                gulag_data = {
                    "Nick": f"{member.name}#{member.discriminator}",
                    "ID": member.id,
                    "Wizyta": 1,
                    "Ilosc wegla": number,
                    "Role": roles_id
                }
                json.dump(gulag_data, file, indent='\t')
        else:
            with open(f"db/gulag/{member.id}.json", "r+") as file:
                gulag_data = json.load(file)
                file.truncate(0)
                file.seek(0)
                gulag_data["Wizyta"] += 1
                gulag_data["Ilosc wegla"] += number
                gulag_data["Nick"] = f"{member.name}#{member.discriminator}"
                gulag_data["Role"] = roles_id
                json.dump(gulag_data, file, indent='\t')

        await member.remove_roles(*roles)
        await member.add_roles(glg_role, reason=f"Zesłano do gułagu przez {ctx.author.name}. \nIlość węgla do wykopania - {number}")

        with open(f"db/gulag/{member.id}.json", "r") as file:
            gulag_data = json.load(file)

        await logs_channel.send(f"""
-=- ⛏️ *Otwarcie rejestru!* ⛏️ -=-

**Personel**: {ctx.author.mention}
**Skazany**: {member.mention}
**Ilość węgla**: {number} kilo | {gulag_data["Ilosc wegla"]} kilo łącznie
**Wizyty**: {gulag_data["Wizyta"]}

-=- ⛏️ *Koniec rejestru!* ⛏️ -=-""")
        await welcome_channel.send(gulag_welcome_message.format(user=member.mention, wegiel=number, wegiel_lacznie=gulag_data["Ilosc wegla"], visit=gulag_data["Wizyta"]))
        await ctx.reply("Zesłano do gułagu.", mention_author=False, delete_after=10.0)
        await sleep(10)
        await ctx.message.delete()
            

    @gulag.error
    async def gulag_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}gulag <ID/@Użytkownik> <Liczba>\n```", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.CheckAnyFailure):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")
            raise error
        
    @bot.command(aliases=["ungułag", "unglg", "ungłg", "ugułag", "uglg", "ugłg"])
    @commands.check_any(commands.has_any_role(*gulag_staff), commands.has_guild_permissions(administrator=True))
    async def ungulag(self, ctx, user):
        if ctx.message.mention_everyone:
            await ctx.reply("Na co liczysz?", mention_author=False, delete_after=15.0)
            return
        
        if len(ctx.message.mentions) > 1:
            await ctx.reply("Możesz podać tylko jednego użytkownika.", mention_author=False, delete_after=15.0)
            return
        elif len(ctx.message.mentions) == 0:
            try:
                user = int(user)
            except ValueError as e:
                await ctx.reply("Podane ID nie jest poprawne.", mention_author=False, delete_after=15.0)
                return

            member = ctx.guild.get_member(user)
            if member is None:
                await ctx.reply("Nie znaleziono użytkownika.", mention_author=False, delete_after=15.0)
                return
        else:
            member = ctx.message.mentions[0]


        logs_channel = ctx.guild.get_channel(gulag_logs)
        if logs_channel is None:
            await ctx.reply(f"Błąd w konfiguracji, nie znaleziono kanału do logów o ID {gulag_logs}.", mention_author=False, delete_after=15.0)
            return

        glg_role = ctx.guild.get_role(gulag_role)
        if glg_role == None:
            await ctx.reply(f"Błąd w konfiguracji, nie znaleziono gułag roli o ID {gulag_welcome_channel}.", mention_author=False, delete_after=15.0)
            return
        if glg_role not in member.roles:
            await ctx.reply("Ten użytkownik nie jest w gułagu.", mention_author=False, delete_after=15.0)
            return

        with open(f"db/gulag/{member.id}.json", "r") as file:
                gulag_data = json.load(file)
                glg_roles = gulag_data["Role"]

        await member.remove_roles(glg_role, reason=f"Wypuszczono z gułagu przez {ctx.author.name}.")
        roles = []
        for taken_role in glg_roles:
            role = ctx.guild.get_role(taken_role)
            roles.append(role)
        await member.add_roles(*roles)

        await logs_channel.send(f"""
-=- :white_check_mark:  *Otwarcie rejestru!* :white_check_mark: -=-

**Personel**: {ctx.author.mention}
**Wypuszczony**: {member.mention}

-=- :white_check_mark:  *Koniec rejestru!* :white_check_mark: -=-""")
        await ctx.reply("Wypuszczono z gułagu.", mention_author=False, delete_after=10.0)
        await sleep(10)
        await ctx.message.delete()
            

    @ungulag.error
    async def ungulag_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}ungulag <ID/@Użytkownik>\n```", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.CheckAnyFailure):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")
            raise error

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if gulag_role == [] or str(gulag_role) == "":
            return
        roles = list(map(lambda r: r.id, member.roles))
        if gulag_role in roles:
            logs_channel = self.bot.get_channel(gulag_logs)
            description = f"""
:exclamation:  *Ucieczka!*  :exclamation:

**Użytkownik**: {member.mention} ({member.id})"""
            embed=discord.Embed(description=description, color=0xe74c3c, timestamp=datetime.now())
            embed.set_author(name="Ochrona Gułagu")
            embed.set_footer(text="ThemePark Gułag System", icon_url=footer_img)
            await logs_channel.send(embed=embed)

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Gulag(bot, intents=intents))