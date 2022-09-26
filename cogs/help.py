from datetime import datetime
import discord, json, os.path
from discord.ext import commands
from asyncio import sleep

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    p = prefix
    administrators = data["administrators"]
    moderators = data["moderators"]
    owner_id = data["ownerID"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]


class Help(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot
        self.lista_cogow = ["frekwencja", "ustawienia", "kartkówki i sprawdziany", "kartkówki i sprawdziany", "oceny", "zadania domowe", "numerek", "plan Lekcji", "pozostałe", "pozostale"]
        self.lista_komend = ["daty", "data", "dni", "tygodnie", "help", "komendy", "pomoc", "cmds", "frekwencja", "obecność", "obecnosc", "ob", "obecny", "nieobecności", "nieobecnosci", "setup", "testy", "tests", "sprawdziany", "spr", "kartkówki", "kartkowki", "kartk", "grades", "oceny", "grade", "ocena", "homework", "zadania_domowe", "zadane", "zadaniadomowe", "zaddom", "hw", "numer", "numerek", "szczęśliwynumerek", "szczesliwynumerek", "luckynumber", "plan", "lekcje", "planlekcji"]


    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)
    staff = administrators + moderators

    @bot.command()
    async def help(self, ctx):
        tmp = f"""**Hej!** 
Poniżej znajdziesz listę {len(self.bot.cogs)} cogów, które zawierają {len(self.bot.commands)} komend. 
~~Jeśli potrzebujesz, możesz uzyskać informacje o wybranej komendzie/kategorii podając jej nazwę jako argument.~~

`<>` oznacza wymagane argumenty
`()` oznacza opcjonalne argumenty"""
        embed=discord.Embed(description=tmp, color=0xdaa454, timestamp=ctx.message.created_at)
        embed.set_author(name=self.bot.user.name)
        embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
        
        cogs = []
        for cog in self.bot.cogs:
            cogs.append(cog)
        cogs.sort()

        for cog in cogs:
            cog_class = self.bot.get_cog(str(cog))
            cmds = len(cog_class.get_commands())
            events = len(cog_class.get_listeners())
            # cmd_help = ""
            # for cmd in self.bot.commands:
            #     if cmd.cog_name == cog:
            #         cmd_help += f"{p}{cmd.name} {cmd.brief}\n"
            #     if len(cog2.get_commands()) > 3:
            #         cmd_help = f"Aby zobaczyć wszystkie komendy, użyj `{p}help <{cog}>`"
            # if cmd_help == "":
            #     cmd_help = "Brak komend"
            # print(cmd_help)
            if cmds == 0:
                cmds = ""
            else:
                cmds = f"Komendy: `{cmds}`\n"

            if events == 0:
                events = ""
            else:
                events = f"Eventy: `{events}`\n"
            
            embed.add_field(name=f"**{cog}**", value=f"{events}{cmds}", inline=True)
        commands = []
        for command in self.bot.commands:
            commands.append(command.name)

        await ctx.reply(embed=embed, mention_author=False)
            
    # @bot.command(aliases=["komendy", "commands"])
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    # async def help(self, ctx, komenda):
    #     komenda = komenda.lower()
    #     if komenda not in self.lista_komend:
    #         if komenda in self.lista_cogow:
    #             await self.show_cog_info(ctx, komenda)
    #             return
    #         else:
    #             tmp = "Nie znaleziono podanej komendy. Czy chcesz wyświetlić główną stronę?"
    #             embed=discord.Embed(description=tmp, color=0xdaa454, timestamp=ctx.message.created_at)
    #             embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
    #             embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
    #             await ctx.send(embed=embed, view=self.NotFound_Button(ctx))
    #             return
    #     else:
    #         await self.show_command_info(ctx, komenda)

    # @help.error
    # async def help_error(self, ctx, error):
    #     if isinstance(error, commands.errors.CommandInvokeError):
    #         error = error.original
    #     if isinstance(error, commands.errors.MissingRequiredArgument):
    #         if error.param.name == "komenda":
    #             await Help.show_main_page(Help, ctx)
    #     elif isinstance(error, commands.errors.MissingPermissions):
    #         await ctx.send("Brak uprawnień!")
    #         raise error
    #     else:
    #         await ctx.send(f"**Wystąpił błąd!** Treść: \n```{error}```")

    
    class RemoveEmbed_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx
        
        @discord.ui.button(label="Usuń", style=discord.ButtonStyle.red)
        async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.ctx.author == interaction.user:
                await self.ctx.message.delete()
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)

    class NotFound_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx

        @discord.ui.button(label="Tak", style=discord.ButtonStyle.green)
        async def tak(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
                await self.ctx.reply(f'{await Help.show_main_page(Help, self.ctx)}', ephemeral=False)
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
        
        @discord.ui.button(label="Nie", style=discord.ButtonStyle.red)
        async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)


async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Help(bot, intents=intents))