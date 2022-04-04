import json
from pydoc import describe
import discord
from discord.ext import commands

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

##########
# Ticket #
##########



    @bot.command(name='24h') 
    async def _24h(self, ctx):
        lastMessage = await ctx.channel.history(limit=100).flatten()
        urlText = ""
        if "Twój ticket właśnie został utworzony" in lastMessage[-1].content:
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="Kliknij mnie!", url=lastMessage[-1].jump_url, style=discord.ButtonStyle.url))
            urlText = "\nPrzejdziesz do reakcji klikając poniższy przycisk."
        description = f"""**Ticket zostanie zamknięty z powodu nieaktywności przez 24 godziny!**
W przypadku ciągłego występowania problemu, odpisz na ticket.\n
Jeśli to wszystko, zamknij proszę ticket klikając :lock: oraz potwierdzając :white_check_mark:.{urlText}"""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        if urlText == "":
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, view=view)

    @_24h.error
    async def _24h_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply("Nie podano wszystkich argumentów!", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

    @bot.command(aliases=["weekend", "cierpliwości", "cierpliwosci", "cierpliwość"])
    async def cierpliwosc(self, ctx):
        description = """
Niestety, nie jesteśmy w stanie odpowiadać regularnie na wszystkie tickety. Każdy z nas ma swoje prywatne życie, zainteresowania, pracę czy szkołę. 
Postaramy się odpowiedzieć, gdy ktoś z nas znajdzie chociaż chwilkę czasu.

Za utrudnienia serdecznie przepraszamy.
        """
        embed=discord.Embed(title="PolishEmergencyV", description=description, color=0x2a44ff)
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @bot.command(aliases=["pomoc"]) 
    async def kanalpomocy(self, ctx):
        description = """<#531964192207405096>"""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_image(url="https://media.giphy.com/media/n9CMNbvOSY4MQGWcon/giphy.gif")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @bot.command(aliases=["nodetails", "brakdetali", "helpme"])
    async def pomusz(self, ctx):
        embed=discord.Embed(title="Pomusz mi! Nie umiem udzielić informacji", color=0x2a44ff)
        embed.set_image(url="https://cdn.discordapp.com/attachments/690185755989114885/911343294850682920/pomusz_mi.png")
        await ctx.message.delete()
        await ctx.send(embed=embed)
    
    @bot.command() 
    async def zamknij(self, ctx):
        lastMessage = await ctx.channel.history(limit=100).flatten()
        urlText = ""
        if "Twój ticket właśnie został utworzony" in lastMessage[-1].content:
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="Kliknij mnie!", url=lastMessage[-1].jump_url, style=discord.ButtonStyle.url))
            urlText = "\nPrzejdziesz do reakcji klikając poniższy przycisk."
        embed=discord.Embed(description=f"Jeśli to wszystko, zamknij proszę ticket klikając :lock: oraz potwierdzając :white_check_mark:. {urlText}", color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        if urlText == "":
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, view=view)\

###############
# Modyfikacje #
###############

    @bot.command() 
    async def els(self, ctx):
        description = """**Spis błędów**

**1.** ELS nie działa!
**2.** ELS Key Lock Active w prawym dolnym rogu
**3.** Światła nie błyskają, działa tylko cruise mode."""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text="!els", icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=self.ELS_Button(ctx))

    class ELS_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx
        @discord.ui.button(label="Spis", style=discord.ButtonStyle.blurple)
        async def home(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**Spis błędów**

**1.** ELS nie działa!
**2.** ELS Key Lock Active w prawym dolnym rogu
**3.** Światła nie błyskają, działa tylko cruise mode."""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text="!els", icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)
        @discord.ui.button(label="Nr. 1", style=discord.ButtonStyle.grey)
        async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**1. ELS nie działa!**
            Upewnij się że masz zainstalowany: 
- ScriptHookV (http://www.dev-c.com/gtav/scripthookv/)
- AdvancedHook (ten przychodzi z ELSem)"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text="!els", icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Nr. 2", style=discord.ButtonStyle.grey)
        async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**2. ELS Key Lock Active**
Wciśnij Scroll Lock."""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text="!els", icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Nr. 3", style=discord.ButtonStyle.grey)
        async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**3. Światła nie błyskają, działa tylko cruise mode.**
        
- Włącz OpenIV
- Tools -> ASI Manager
- Odinstaluj wszytkie opcje
- Odinstaluj OpenIV
- Zrestartuj komputer
- Zainstaluj OpenIV od nowa
- Zainstaluj pierwsze dwie opcje w ASI Manager
- Sprawdź w grze"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text="!els", icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Usuń", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)

    @bot.command() 
    async def gameconfig(self, ctx):
        description = """**1. Jak zainstalować gameconfig?**
Na kanale <#690184232097939591> są dwa filmy zrobione przez nas, część pierwsza pokazuje instalację gameconfigu.
Wybierz wersję "More Mods".

**2. Co to jest X traffic i ped?**
#x to jest mnożnik danej wartości; 
- Traffic odpowiada za wielkość ruchu samochodów, 
- Ped odpowiada za ilość NPC na ulicy. 
Stock to domyślne wartości GTA.

**3. Gdzie jest gameconfig?**
`mods -> update -> update.rpf -> common -> data`

**Link**
https://pl.gta5-mods.com/misc/gta-5-gameconfig-300-cars"""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text="!gameconfig", icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @bot.command() 
    async def lspdfr(self, ctx):
        description = """**LSPD: First Response**
Zalecamy użycie Manualnej Instalacji!"""
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Link do pobrania", url="https://lcpdfr.com/downloads/gta5mods/g17media/7792-lspd-first-response/", style=discord.ButtonStyle.url))
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text="!lspdfr", icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=view)

    @bot.command(aliases=["rnui"]) 
    async def ragenativeui(self, ctx):
        description = """**Rage Native UI**
Plik `RageNativeUI.dll` przenosisz do głównego folderu GTA V (tam gdzie GTAV.exe).
Nie podmieniaj tego pliku, gdy instalujesz cokolwiek innego."""
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Link do pobrania", url="https://github.com/alexguirre/RAGENativeUI/releases/latest", style=discord.ButtonStyle.url))
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text="!rnui", icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=view)

    @bot.command(aliases=["rage", "ragepluginhook"]) 
    async def rph(self, ctx):
        description = """**Spis błędów**\n
    
**1.** Plugin "XXX" was terminated because it caused the game to freeze?
**2.** Insufficient Permissions or Bad Antivirus"""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text="!rph", icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=self.RPH_Button(ctx))

    class RPH_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx
        @discord.ui.button(label="Spis", style=discord.ButtonStyle.blurple)
        async def home(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**Spis błędów**\n
            
**1.** Plugin "XXX" was terminated because it caused the game to freeze?
**2.** Insufficient Permissions or Bad Antivirus"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text="!rph", icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)
        @discord.ui.button(label="Nr. 1", style=discord.ButtonStyle.grey)
        async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**1. Plugin "XXX" was terminated because it caused the game to freeze?**
Podczas włączania RagePluginHooka kliknij ikonkę Ustawień (trybik), a następnie w polu "Plugin Timeout Threshold" wpisz "60000" (4 zera)."""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text="!rph", icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Nr. 2", style=discord.ButtonStyle.grey)
        async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**2. Insufficient Permissions or Bad Antivirus**
Są 2 zasady:
- Nie możesz włączać GTA z innego folderu niż oryginalnie zainstalowałeś. 
- Nie możesz zmieniać nazwy folderu.

Na początek postaraj się wyłączyć wszystkie antywirusy, później aplikacje które mogą przyśpieszać gry (np. Razer Cortex, RivaTuner).
Jeśli nadal nie podziałało kliknij prawym na GTA5.exe -> Właściwości -> Zabezpieczenia. Upewnij się że SYSTEM, Administratorzy oraz twój użytkownik posiadają wszystkie uprawnienia (możesz zignorować "Uprawnienia specjalne").
Jeśli tak nie jest, kliknij przycisk "Edytuj" i dodaj im brakujące uprawnienia.

Spróbuj teraz włączyć grę."""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text="!rph", icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Usuń", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)

    @bot.command(aliases=["shv", "scripthook"])
    async def scripthookv(self, ctx):
        description = """**ScriptHookV**
Przesuń pliki `ScriptHookV.dll` oraz `dinput8.dll` do głównego folderu z grą."""
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Link do pobrania", url="http://www.dev-c.com/gtav/scripthookv/", style=discord.ButtonStyle.url))
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text="!scripthook", icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=view)

    @bot.command(aliases=["eup", "peup", "ciuchy"]) 
    async def stroje(self, ctx):
        description = """**Spis błędów**

**1.** Mieszają mi się stroje z amerykańskimi
**2.** Zainstalowałem automatycznym instalatorem i są dziwne stroje oraz stare jednostki w LSPDFR
**3.** Mam polskie jednostki, ale dziwne stroje.
**4.** Konfig do UltimateBackup"""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=self.EUP_Button(ctx))

    class EUP_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx
        # primary/blurple = 1
        # secondary/grey/gray = 2
        # success/green = 3
        # danger/red = 4
        # link/url = 5
        @discord.ui.button(label="Spis", style=discord.ButtonStyle.blurple)
        async def home(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**Spis błędów**

**1.** Mieszają mi się stroje z amerykańskimi
**2.** Zainstalowałem automatycznym instalatorem i są dziwne stroje oraz stare jednostki w LSPDFR
**3.** Mam polskie jednostki, ale dziwne stroje.
**4.** Konfig do UltimateBackup"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self, embed=embed)
        @discord.ui.button(label="Nr. 1", style=discord.ButtonStyle.grey)
        async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**1. Mieszają mi się stroje z amerykańskimi**
- w OpenIV usuń folder EUP z `update -> x64 -> dlcpacks`
- Zainstaluj ponownie PEUP bez instalacji EUP L&O i S&R"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Nr. 2", style=discord.ButtonStyle.grey)
        async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**2. Zainstalowałem automatycznym instalatorem i są dziwne stroje oraz stare jednostki w LSPDFR**
Zainstaluj konfigi, które są w tym samym archiwum co instalator."""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Nr. 3", style=discord.ButtonStyle.grey)
        async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**3. Mam polskie jednostki, ale dziwne stroje.**
Zainstaluj od nowa pliki konfiguracyjne oraz stroje. Nie instaluj EUP Law&Order czy Server&Rescue."""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self, embed=embed)
        
        @discord.ui.button(label="Nr. 4", style=discord.ButtonStyle.grey)
        async def four(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**4. Konfig do UltimateBackup**
[LSPDFR.com](https://www.lcpdfr.com/downloads/gta5mods/misc/29319-ultimate-backup-config-for-polish-eup-polskie-stroje-dla-ultimate-backup/ 'Kliknij by przejść do LSPDFR.com!')
[Nasza strona](https://polishemergencyv.com/file/3-ultimate-backup-config-for-polish-eup/ 'Kliknij by przejść do PolishEmergencyV.com!')"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Usuń", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)

##############
# Instrukcje #
##############

    @bot.command(aliases=["crashe", "crashfaq", "błędy", "błedy", "bledy", "blędy"]) 
    async def crash(self, ctx):
        description = """**Spis Crashy**
    
**1.** Zainstalowałem pojazdy i crashuje
**2.** Crashuje, a nie mam folderu mods. Jak usunę ELS.asi to działa. RPH crashuje mi całą grę.
**3.** Błąd ERR_MEM_EMBEDDEDALLOC_ALLOC
**4.** Błąd ERR_FIL_PACK_1"""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=self.Crash_Button(ctx))

    class Crash_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx
        @discord.ui.button(label="Spis", style=discord.ButtonStyle.blurple)
        async def home(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**Spis Crashy**
    
**1.** Zainstalowałem pojazdy i crashuje
**2.** Crashuje, a nie mam folderu mods. Jak usunę ELS.asi to działa, plik RagePluginHook.log się nie generuje.
**3.** Błąd ERR_MEM_EMBEDDEDALLOC_ALLOC
**4.** Błąd ERR_FIL_PACK_1"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Nr. 1", style=discord.ButtonStyle.grey)
        async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**1. Zainstalowałem pojazdy i crashuje**
Upewnij się, że masz zainstalowany gameconfig. Link do jego pobrania znajdziesz [tutaj](https://pl.gta5-mods.com/misc/gta-5-gameconfig-300-cars) lub na <#531964192207405096>"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Nr. 2", style=discord.ButtonStyle.grey)
        async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**2. Crashuje, a nie mam folderu mods. Jak usunę ELS.asi to działa, plik RagePluginHook.log się nie generuje.**
Zrestartuj grę, a następnie przejdź do folderu z plikami gry. Kliknij prawym przyciskiem na folder zawierający pliki GTA. 
Wybierz Właściwości -> Zabezpieczenia -> Edytuj -> Użytkownicy -> Pełna kontrola. Kliknij Zastosuj, a następnie OK."""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Nr. 3", style=discord.ButtonStyle.grey)
        async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**3. Błąd ERR_MEM_EMBEDDEDALLOC_ALLOC**
Zainstaluj HeapAdjuster. Link znajdziesz [tutaj](https://www.gta5-mods.com/tools/heapadjuster) lub na <#531964192207405096>"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Nr. 4", style=discord.ButtonStyle.grey)
        async def four(self, button: discord.ui.Button, interaction: discord.Interaction):
            description = """**4. Błąd ERR_FIL_PACK_1**
Zainstaluj PackfileLimitAdjuster. Link znajdziesz [tutaj](https://www.gta5-mods.com/tools/packfile-limit-adjuster) lub na <#531964192207405096>"""
            embed=discord.Embed(description=description, color=0x2a44ff, timestamp=self.ctx.message.created_at)
            embed.set_author(name="PolishEmergencyV")
            embed.set_footer(text=footer, icon_url=footer_img)
            await interaction.response.edit_message(view=self, embed=embed)

        @discord.ui.button(label="Usuń", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
    
    @bot.command(aliases=["czystyfolder"]) 
    async def czystegta(self, ctx):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Steam", url="https://i.imgur.com/LssMtWG.png", style=discord.ButtonStyle.url))
        view.add_item(discord.ui.Button(label="Epic Games", url="https://i.imgur.com/tNLuM7Y.png", style=discord.ButtonStyle.url))
        view.add_item(discord.ui.Button(label="Rockstar Launcher", url="https://i.imgur.com/yaQbqOi.png", style=discord.ButtonStyle.url))
        embed=discord.Embed(description=f"Poniżej znajdziesz przyciski, które przekierują cię do obrazka z czystym folderem GTA do każdej platformy.", color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=view)

    @bot.command() 
    async def dlclist(self, ctx):
        description = """Wyślij screena lub zawartość pliku dlclist.xml znajdującego się w tej lokalizacji: \n`mods -> update -> update.rpf -> common -> data`"""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @bot.command() 
    async def log(self, ctx):
        description = """Zostałeś poproszony o wysłanie zawartości pliku RagePluginHook.log. Plik znajdziesz w głównym folderze gry, i jest on oznaczony jako plik tekstowy."""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_image(url="https://cdn.discordapp.com/attachments/741061366357557298/841052997982355456/unknown.png")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)

########
# Inne #
########

    @bot.command() 
    async def fivem(self, ctx):
        description = """   Obecnie pracujemy nad paczką naszych modów zoptymalizowaną specjalnie pod FiveM. Prace jednak trwają, dlatego postanowiliśmy zawiesić wydawanie nowych zgód. 
Radzimy jednak poczekać i obserwować kanał ogłoszeń. Postaramy się by w tym roku pojawiły się tam pierwsze informacje oraz zapowiedzi odnośnie wspomnianej paczki. 
Warto poczekać, ponieważ nasze pojazdy będą się cechowały wybitną optymalizacją oraz jakością. Dla serwerów chcących skorzystać z wspomnianej paczki będziemy również oferować dodatkową pomoc oraz pewne bonusy, na razie, prosimy o uzbrojenie się w cierpliwość :wink:"""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)
    
    @bot.command(aliases=["license"]) 
    async def licencja(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://polishemergencyv.com/licencja")

    @bot.command(aliases=["zmodeler3", "zmodeler2"]) 
    async def zmodeler(self, ctx):
        description = """Nie świadczymy pomocy w tworzeniu własnych modyfikacji. Internet oferuje poradniki oraz fora, tworzenie modyfikacji to nie jest bułka z masłem. 
Uprzedzając, nie polecimy żadnego poradnika, nie pomożemy Ci prywatnie, a ten serwer nie posiada tematyki pomocy w tworzeniu modów. 
Liczymy na wyrozumiałość."""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)
    

    @bot.command() 
    async def faq(self, ctx):
        description = """**Lista komend FAQ**
--- Ticket ---
- 24h
- cierpliwosc/cierpliwosci
- kanalpomocy / pomoc
- pomusz / brakdetali / helpme
- zamknij

--- Modyfikacje ---
- els
- gameconfig
- lspdfr
- ragenativeui / rnui
- ragepluginhook / rph
- scripthook / shv
- stroje / eup / peup / ciuchy

--- Instrukcje ---
- crash
- czystyfolder
- dlclist
- log

--- Inne ---
- fivem
- licencja
- zmodeler / zmodeler3
"""
        embed=discord.Embed(description=description, color=0x2a44ff, timestamp=ctx.message.created_at)
        embed.set_author(name="PolishEmergencyV")
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FAQ(bot))