import discord, json, re, requests
from typing import Optional
from discord.ext import commands
from asyncio import sleep

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]
    administrators = data["administrators"]
    moderators = data["moderators"]
    steam_api_key = data["steam_api"]

with open("configs/themeparkConfig.json", "r") as config:
    data = json.load(config)
    sl_staff = data["game_staff"]
    gban_log = data["gban_log_message"]
    gban_message = data["gban_message"]
    gameban_channel = data["gban_channel"]
    gameban_logs = data["gban_logs"]

class GameBan(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    staff = administrators + sl_staff

    @bot.command(aliases=["gameban", "goban", "gameofflineban"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(administrator=True))
    async def gban(self, ctx, id, time, *, reason: Optional[str] = "Brak powodu."):
        gban_channel = ctx.guild.get_channel(gameban_channel)
        if gban_channel is None:
            await ctx.reply(f"Błąd w konfiguracji, nie znaleziono kanału do wysłania gbana o ID {gameban_channel}.", mention_author=False, delete_after=30.0)
            return

        gban_logs = ctx.guild.get_channel(gameban_logs)
        if gban_channel is None and gameban_logs != 0:
            await ctx.reply(f"Błąd w konfiguracji, nie znaleziono kanału do wysłania logów gbana o ID {gameban_channel}.", mention_author=False, delete_after=30.0)
            return
        
        if not re.match(r"^([0-9]{17}@steam|[0-9@]{17,18}@discord)$", id):
            await ctx.reply("Podano błędne ID.", mention_author=False, delete_after=10.0)
            return

        if not re.match(r"^[0-9]*(m|h|d|w|y){1}$", time):
            await ctx.reply("Podano błędny czas, m/h/d/w/y.", mention_author=False, delete_after=10.0)
            return

        if "@discord" in id:
            nick = f"<@{id.split('@')[0]}>"
        else:
            steamid = id.split('@')[0]
            api = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key={steam_api_key}&steamids={steamid}")
            api = api.json()

            if str(api['response']['players']['player'][0]) == "None":
                nick = "API Error"
            else:
                nick = api['response']['players']['player'][0]['personaname']

        if gameban_logs != 0:
            await gban_logs.send(gban_log.format(nick=nick, id=id, reason=reason, time=time, staff=ctx.author.mention))

        await gban_channel.send(gban_message.format(id=id, reason=reason, time=time, staff=f'{ctx.author.name}#{ctx.author.discriminator}'))
        await ctx.reply("Zbanowano.", mention_author=False, delete_after=10.0)
        await sleep(10)
        await ctx.message.delete()
            

    @gban.error
    async def gban_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}gban <SteamID@steam / DiscordID@steam> <Czas w m/h/d/w> <Powód>\n```", mention_author=False)
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
        

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(GameBan(bot, intents=intents))