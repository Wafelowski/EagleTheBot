from datetime import datetime
import discord, json, os
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from asyncio import sleep

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

class Patreon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command()
    @has_permissions(administrator=True)  
    async def patreoncleanup(self, ctx, confirmation):
        # if ctx.guild.id != "531961175114645534":
        #     await ctx.reply("Komenda nie jest dostępna na tym serwerze!", mention_author=False)
        #     return
        if confirmation != "confirm":
            await ctx.reply("Komendę trzeba potwierdzić dodając argument `confirm` do komendy!", mention_author=False)
            return
        wspierajacy = ctx.guild.get_role(860610858949672970) # PEV wspierajacy - 531965941958049833
        sierzant = ctx.guild.get_role(860543081324478474) # PEV sierzant - 531965941958049833
        aspirant = ctx.guild.get_role(861924070478839829) # PEV aspirant - 531965941958049833
        members_list = []
        sierzant_list = []
        aspirant_list = []
        i = 0
        for member in wspierajacy.members:
            if i == 4:
                print("---------------- \nPatreon rate limit - waiting 5 seconds \n----------------\n")
                await sleep(5)
                i = 0
            print(member.name + "#" + member.discriminator)
            members_list.append(member.id)
            if member in sierzant.members:
                sierzant_list.append(member.id)
                print("Sierzant")
                await member.remove_roles(*[wspierajacy, sierzant], reason=f"[Sierzant] \nPatreon Cleanup, ran by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
            elif member in aspirant.members:
                aspirant_list.append(member.id)
                print("Aspirant")
                await member.remove_roles(*[wspierajacy, aspirant], reason=f"[Aspirant] \nPatreon Cleanup, ran by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
            else:
                print("Wspierajacy")
                await member.remove_roles(wspierajacy, reason=f"Patreon Cleanup, ran by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
            i = i+1
            print("---------------\n")
        print(f"Lista wspierajacych: {members_list}")
        print(f"Lista sierzantow: {sierzant_list}")
        print(f"Lista aspirantow: {aspirant_list}")
        date = datetime.strftime(datetime.now(), '%d-%m %H-%M-%S')
        if not os.path.exists("./patreon"):
            os.mkdir("patreon")
        with open(f"patreon/supporters_list - {date}.txt", "w") as temp:
            temp.write(str(members_list).replace("[", "").replace("]", "").replace(", ", "\n"))
        with open(f"patreon/sierzant_list - {date}.txt", "w") as temp:
            temp.write(str(sierzant_list).replace("[", "").replace("]", "").replace(", ", "\n"))
        with open(f"patreon/aspirant_list - {date}.txt", "w") as temp:
            temp.write(str(aspirant_list).replace("[", "").replace("]", "").replace(", ", "\n"))


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

def setup(bot):
    bot.add_cog(Patreon(bot))