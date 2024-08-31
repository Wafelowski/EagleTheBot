from datetime import datetime
import discord, json, os, tomli
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from asyncio import sleep

# Role1 is the main role for this cog, usually named Supporter. Command goes through members of this role.
# Role2 and Role3 and some additional roles, usually named after tiers. These roles are removed additionaly to the main role.

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]

with open("configs/pevConfig.toml", "rb") as config:
    data = tomli.load(config)
    role1 = data["patreon"]["role_1"]
    role2 = data["patreon"]["role_2"]
    role3 = data["patreon"]["role_3"]

class Patreon(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @bot.command()
    @has_permissions(administrator=True)
    async def patreoncleanup(self, ctx, confirmation):
        if confirmation != "confirm":
            await ctx.reply("Komendę trzeba potwierdzić dodając argument `confirm` do komendy!", mention_author=False)
            return

        role1 = ctx.guild.get_role(role1)
        role2 = ctx.guild.get_role(role2)
        role3 = ctx.guild.get_role(role3)

        role1_list = []
        role2_list = []
        role3_list = []
        i = 0
        for member in role1.members:
            if i == 4:
                print("---------------- \nPatreon rate limit - waiting 5 seconds \n----------------\n")
                await sleep(5)
                i = 0
            print(member.name + "#" + member.discriminator)
            role1_list.append(member.id)
            if member in role2.members:
                role2_list.append(member.id)
                await member.remove_roles(*[role1, role2], reason=f"[Role 1] \nPatreon Cleanup, ran by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
            elif member in role3.members:
                role3_list.append(member.id)
                await member.remove_roles(*[role1, role3], reason=f"[Role 3] \nPatreon Cleanup, ran by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
            else:
                await member.remove_roles(role1, reason=f"Patreon Cleanup, ran by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
            i = i+1
            print("---------------\n")
        print(f"Lista pierwszej roli: {role1_list}")
        print(f"Lista drugiej roli: {role2_list}")
        print(f"Lista trzeciej roli: {role3_list}")
        date = datetime.strftime(datetime.now(), '%d-%m %H-%M-%S')
        if not os.path.exists("./patreon"):
            os.mkdir("patreon")
        with open(f"patreon/role1_list - {date}.txt", "w") as temp:
            temp.write(str(role1_list).replace("[", "").replace("]", "").replace(", ", "\n"))
        with open(f"patreon/role2_list - {date}.txt", "w") as temp:
            temp.write(str(role2_list).replace("[", "").replace("]", "").replace(", ", "\n"))
        with open(f"patreon/role3_list - {date}.txt", "w") as temp:
            temp.write(str(role3_list).replace("[", "").replace("]", "").replace(", ", "\n"))


    @patreoncleanup.error
    async def patreon_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}patreoncleanup confirm\n```", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Patreon(bot, intents=intents))