import discord, tomli, re, requests
from typing import Optional
from datetime import datetime
from discord.ext import commands
from asyncio import sleep

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]
    steam_api_key = data["api"]["steam_api"]


class SteamUtils(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @bot.command(aliases=["steamprofile"])
    async def steam(self, ctx, sid):

        if re.search(r"(.*\/\/steamcommunity\.com\/profiles\/)?([0-9]{17})", sid):
            sid = int(sid[-17:])

        elif re.match(r"^STEAM_[0-5]:[0-1]:[0-9]{8,9}$", sid):
            steamid64 = 76561197960265728
            sid = sid.split(":")
            steamid64 += int(sid[2]) * 2 
            if sid[1] == "1":
                steam64id += 1
            sid = steamid64
        
        else:
            await ctx.reply("Nieprawidłowe SteamID!", mention_author=False)
            return


        api = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key={steam_api_key}&steamids={sid}")
        api = api.json()

        if str(api['response']['players']['player'][0]) == "None":
            await ctx.reply("API nie zwróciło wyniku.", mention_author=False)
            return

        api = api['response']['players']['player'][0]
        nick = api['personaname']
        steamid = api['steamid']
        profileurl = api['profileurl']
        profilestate = api['profilestate']
        if profilestate == 0:
            await ctx.reply("Użytkownik nie posiada profilu.", mention_author=False)
            return

        avatar = api['avatarfull']
        personastate = api['personastate']
        communityvisibilitystate = api['communityvisibilitystate']
        if (communityvisibilitystate == 1) or (communityvisibilitystate == 2):
            communityvisibilitystate = "Prywatny / Dla znajomych"
            personastate = "Nieznane"
            color = 0x68717D
        elif communityvisibilitystate == 3:
            communityvisibilitystate = "Publiczny"
            if personastate == 1:
                personastate = "Online"
                color = 0x3EA25E
            elif personastate == 2:
                personastate = "Zajęty"
                color = 0xE94649
            elif personastate == 3:
                personastate = "Zaraz wracam"
                color = 0xF4A620
            elif personastate == 4:
                personastate = "Drzemka"
                color = 0xF4A620
            elif personastate == 5:
                personastate = "Chętny do wymiany"
                color = 0x3EA25E
            elif personastate == 6:
                personastate = "Chętny do rozgrywki"
                color = 0x3EA25E
            else:
                personastate = "Offline"
                color = 0x68717D

            realname = api['realname']
            timecreated = datetime.utcfromtimestamp(api['timecreated']).strftime("%d.%m.%Y %H:%M")
            lastlogoff = datetime.utcfromtimestamp(api['lastlogoff']).strftime("%d.%m.%Y %H:%M")
            if personastate != "Offline":
                lastlogoff = "Online"
            if "gameextrainfo" in api:
                game = api['gameextrainfo']
            else:
                game = None

            friends = requests.get(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={steam_api_key}&steamid={sid}&relationship=friend")
            friends = friends.json()
            if str(friends) != r"{}":
                friends = len(friends['friendslist']['friends'])
            else:
                friends = "Prywatne"

            games = requests.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={sid}")
            games = games.json()
            if str(games['response']) != r"{}":
                games = games['response']['game_count']
            else:
                games = "Prywatne"

        print(nick)

        embed=discord.Embed(title=f"Steam | {nick}", color=color, timestamp=ctx.message.created_at, url=profileurl)
        embed.add_field(name="Nazwa Profilu", value=nick, inline=True)
        if communityvisibilitystate == 3:
            embed.add_field(name="Dopisek", value=realname, inline=True)
        embed.add_field(name="SteamID", value=steamid, inline=True)

        embed.add_field(name="Status", value=personastate, inline=True)
        embed.add_field(name="Prywatność Profilu", value=communityvisibilitystate, inline=True)

        if api['communityvisibilitystate'] == 3:
            embed.add_field(name="Utworzenie konta", value=timecreated, inline=True)
            embed.add_field(name="Ostatnie logowanie", value=lastlogoff, inline=True)

            if game != None:
                embed.add_field(name="Aktualna gra", value=game, inline=False)

            embed.add_field(name="Znajomi", value=friends, inline=True)
            embed.add_field(name="Gry", value=games, inline=True)

        embed.set_thumbnail(url=avatar)
        embed.set_footer(text=footer, icon_url=footer_img)

        await ctx.send(embed=embed, mention_author=False)
        await ctx.message.delete()
            

    @steam.error
    async def steam_error(self, ctx, error):
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
    await bot.add_cog(SteamUtils(bot, intents=intents))