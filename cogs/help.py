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
    async def tester(self, ctx):
        tmp = f"""**Hej!** 
Poniżej znajdziesz listę {len(self.bot.cogs)} cogów, które zawierają {len(self.bot.commands)} komend. 
Jeśli potrzebujesz, możesz uzyskać informacje o wybranej komendzie/kategorii podając jej nazwę jako argument. 

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
                cmds = "Brak"
            if events == 0:
                events = "Brak"
            
            embed.add_field(name=f"**{cog}**", value=f"**Eventy**: {events} \n**Komendy**: {cmds}", inline=True)
        commands = []
        for command in self.bot.commands:
            commands.append(command.name)

        await ctx.reply(embed=embed, mention_author=False)
            

    @bot.command(aliases=["komendy", "commands"])
    @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, komenda):
        komenda = komenda.lower()
        if komenda not in self.lista_komend:
            if komenda in self.lista_cogow:
                await self.show_cog_info(ctx, komenda)
                return
            else:
                tmp = "Nie znaleziono podanej komendy. Czy chcesz wyświetlić główną stronę?"
                embed=discord.Embed(description=tmp, color=0xdaa454, timestamp=ctx.message.created_at)
                embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                await ctx.send(embed=embed, view=self.NotFound_Button(ctx))
                return
        else:
            await self.show_command_info(ctx, komenda)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            if error.param.name == "komenda":
                await Help.show_main_page(Help, ctx)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"**Wystąpił błąd!** Treść: \n```{error}```")

    async def show_main_page(self, ctx):
        tmp = """**Witaj w Wirtualnym Asystencie Lekcyjnym!** 
Poniżej znajdziesz listę komend. Jeśli potrzebujesz, możesz uzyskać informacje o wybranej komendzie/kategorii podając jej nazwę jako argument. 
`<>` oznacza wymagane argumenty
`()` oznacza opcjonalne argumenty"""
        embed=discord.Embed(description=tmp, color=0xdaa454, timestamp=ctx.message.created_at)
        embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
        embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)

        embed.add_field(name="Frekwencja", value=f"`{p}frekwencja <data>`", inline=False)
        embed.add_field(name="Kartkówki i Sprawdziany", value=f"`{p}testy <data>`", inline=False)
        embed.add_field(name="Numerek", value=f"`{p}numerek`", inline=False)
        embed.add_field(name="Oceny", value=f"`{p}oceny`\n`{p}ocena <ID>`", inline=False)
        embed.add_field(name="Plan Lekcji", value=f"`{p}plan <data>`", inline=False)
        embed.add_field(name="Zadania domowe", value=f"`{p}zadane <data>`", inline=False)

        embed.add_field(name="Pozostałe", value=f"`{p}help <komenda>` \n`{p}ping`", inline=False)
        await ctx.reply(embed=embed, view=Help.RemoveEmbed_Button(ctx), mention_author=False)

    async def show_command_info(self, ctx, komenda):
        if komenda in ["frekwencja", "obecność", "obecnosc", "ob", "obecny", "nieobecności", "nieobecnosci"]:
            tmp = f"""\n`{p}frekwencja <data>` \n```ini\n[Aliasy] \n!ob | !obecny | !obecność | !nieobecności \n\n[Argumenty] \n<data> - Akceptowalny system dat, wpisz "!help daty" by uzyskać więcej informacji```"""
            tmp2 = "Frekwencja"
        elif komenda in ["testy", "tests", "sprawdziany", "spr", "kartkówki", "kartkowki", "kartk"]:
            tmp = f"""\n`{p}testy <data>` \n```ini\n[Aliasy] \n!spr | !sprawdziany | !kartk | !kartkówki | !tests \n\n[Argumenty] \n<data/tydzień> - Akceptowalny system dat, wpisz "!help daty" by uzyskać więcej informacji```"""
            tmp2 = "Kartkówki i Sprawdziany"
        elif komenda in ["oceny", "grades", "grade", "ocena"]:
            tmp = f"""\n`{p}oceny` \n```ini\n[Aliasy] \n!grades``` \n`{p}ocena <ID>` \n```ini\n[Aliasy] \n{p}grade \n\n[Argumenty] \n<ID> - Identyfikator oceny pozyskiwany przez komendę !oceny. Znajduje się w nawiasie```"""
            tmp2 = "Oceny"
        elif komenda in ["homework", "zadania_domowe", "zadane", "zadaniadomowe", "zaddom", "hw"]:
            tmp = f"""\n`{p}zadane <data>` \n```ini\n[Aliasy] \n!hw | !homework | !zaddom | !zadaniadomowe | !zadania_domowe \n\n[Argumenty] \n<data> - Akceptowalny system dat, wpisz "!help daty" by uzyskać więcej informacji```"""
            tmp2 = "Zadania Domowe"
        elif komenda in ["numer", "numerek", "szczęśliwynumerek", "szczesliwynumerek", "luckynumber"]:
            tmp = f"""\n`{p}numerek` \n```ini\n[Aliasy] \n!numer | !szczęśliwynumerek | !luckynumber```"""
            tmp2 = "Szczęśliwy Numerek"
        elif komenda in ["plan", "lekcje", "planlekcji"]:
            tmp = f"""\n`{p}plan <data>` \n```ini\n[Aliasy] \n!lekcje | !planlekcji \n\n[Argumenty] \n<data> - Akceptowalny system dat, wpisz "!help daty" by uzyskać więcej informacji```"""
            tmp2 = "Plan Lekcji"
        elif komenda in ["help", "komendy", "pomoc", "cmds"]:
            tmp = f"""\n`{p}help (cmd/kat)` \n```ini\n[Aliasy] \n!cmds | !pomoc | !komendy \n\n[Argumenty] \n(cmd/kat) - Komenda lub kategoria. Listę kategorii oraz komend znajdziesz pod tą właśnie komendą.```"""
            tmp2 = "Pozostałe"
        elif komenda in ["setup"]:
            tmp = f"""\n`{p}setup <token> <symbol> <pin>` \n```ini\n[Opis] \nPozwala na ustawienie konta do dziennika. Użyj "!setup info" by uzyskać instrukcję uzyskania danych do konta. \n\n[Argumenty] \n<token> - Token uzyskiwany podczas tworzenia mobilnego dostępu. 7 znakowy \n<symbol> - Określenie na region dziennika, np. leszno \n<pin> - PIN uzyskiwany razem z tokenem oraz symbolem. 6 znakowy``` \n`{p}delsetup` \n```ini\n[Opis] \nPozwala na usunięcie zapisanego konta.```"""
            tmp2 = "Ustawienia"
        elif komenda in ["daty", "data", "dni", "tygodnie"]:
            tmp = f"""
```asciidoc
[Daty]
- 1.1.21
- 1.1.2021
- 1.10.2021
- 10.1.2021
- 01.10.2021
- 1/1/21
- 1/1/2021
- 1/10/2021
- 10/1/2021
- 01/10/2021
[Dni]
- wczoraj/dzisiaj/jutro/pojutrze
- poniedziałek/wtorek/środa/czwartek/piątek
[Tygodnie]
- dzisiaj/obecny/aktualny/ten_tydzień
- za_tydzień/następny/przyszły
```"""
            tmp2 = "System dat, dni oraz tygodnii"
        else:
            tmp = """Nie udało się znaleźć strony pomocy dla wybranej komendy."""
            tmp2 = "Wystąpił błąd"
            
        embed=discord.Embed(title=tmp2, description=tmp, color=0xdaa454, timestamp=ctx.message.created_at)
        embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
        embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
        await ctx.reply(embed=embed, view=Help.RemoveEmbed_Button(ctx), mention_author=False)

    async def show_cog_info(self, ctx, cog):
        if cog in ["pozostałe", "pozostale"]:
            tmp = f"""\n`{p}help (cmd/kat)` \n```ini\n[Aliasy] \n!cmds | !pomoc | !komendy \n\n[Argumenty] \n(cmd/kat) - Komenda lub kategoria. Listę kategorii oraz komend znajdziesz pod tą właśnie komendą.``` 
`{p}ping` \n```ini\n[Opis] \nPo prostu ping, na co liczysz?```
`{p}wyłącz` \n```ini\n[Opis] \nZamyka proces bota. \n\n[Aliasy] \n{p}off | {p}shutdown```
`{p}przeładuj` \n```ini\n[Opis] \nPrzeładowuje wybrany cog. \n\n[Aliasy] \n{p}reload \n\n[Argumenty] \n<cog> - Nazwa coga.```
"""
            tmp2 = "Pozostałe"
        else:
            tmp = """Nie udało się znaleźć strony pomocy dla wybranej kategorii."""
            tmp2 = "Wystąpił błąd"
            
        embed=discord.Embed(title=tmp2, description=tmp, color=0xdaa454, timestamp=ctx.message.created_at)
        embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
        embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
        await ctx.reply(embed=embed, view=Help.RemoveEmbed_Button(ctx), mention_author=False)

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