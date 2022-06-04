from datetime import datetime
import discord, json, math, time, platform, psutil
from discord.ext import commands
from asyncio import sleep

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    administrators = data["administrators"]
    moderators = data["moderators"]
    owner_id = data["ownerID"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]


class BotUtilities(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot
        
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)
    staff = administrators + moderators

    @bot.command()
    async def botinfo(self, ctx):
        before = time.monotonic()
        msg = await ctx.channel.send("📊 Zbieram informacje...")
        ping = (time.monotonic() - before) * 1000
        
        async with ctx.channel.typing():
            await sleep(2)
            
            events = 0
            for cog in self.bot.cogs:
                events += len(self.bot.get_cog(cog).get_listeners())

            app = await self.bot.application_info()

            channels = 0
            for c in self.bot.get_all_channels():
                channels += 1

            embed=discord.Embed(title=f"📊 | Bot Info", color=discord.Color.random(), timestamp=ctx.message.created_at, url=app.icon.url)
            embed.add_field(name="🐍 | Python", value=platform.python_version(), inline=True)
            embed.add_field(name="🌐 | GitHub", value="[Klik!](https://github.com/HeavyWolfPL/EagleTheBot)")
            embed.add_field(name="👾 | Framework", value=f"[discord.py {discord.__version__}](http://discordpy.readthedocs.io/en/latest/)", inline=True)

            embed.add_field(name="🖥️ | OS", value=platform.system(), inline=True)
            embed.add_field(name="🧠 | CPU", value=f"{psutil.cpu_percent()}%", inline=True)
            embed.add_field(name="📝 | RAM", value=f"{psutil.virtual_memory().percent}%", inline=True)

            embed.add_field(name="🛠️ | Cogi", value=len(self.bot.cogs), inline=True)
            embed.add_field(name="⌨️ | Komendy", value=len(self.bot.commands), inline=True)
            embed.add_field(name="📢 | Eventy", value=events, inline=True)
            
            embed.add_field(name="🏘️ | Serwery", value=len(self.bot.guilds), inline=True)
            embed.add_field(name="🚪 | Kanały", value=channels, inline=True)
            embed.add_field(name="👥 | Użytkownicy", value=len(self.bot.users), inline=True)

            embed.set_thumbnail(url=app.icon.url)
            embed.set_footer(text=f"{footer} | Wersja 2.0", icon_url=footer_img)

            await msg.delete()
            await ctx.reply(embed=embed, view=BotUtilities.RemoveEmbed_Button(ctx), mention_author=False)

    @botinfo.error
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


    @bot.command()
    async def json(self, ctx, *, data):
        try:
            encoded = json.dumps(data)
        except:
            await ctx.send("Wystąpił błąd podczas kodowania danych lub nie można ich zakodować.")
            return
        
        await ctx.reply(content=f"Oto twoja wiadomość zamieniona na JSON: \n```json\n{encoded}\n```", view=BotUtilities.RemoveEmbed_Button(ctx), mention_author=False)
        
    @json.error
    async def json_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Musisz podać treść!")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

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

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(BotUtilities(bot, intents=intents))