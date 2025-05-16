# import discord, json, os, tomli
# from discord.ext import commands

# # from main import sendError # BUG: Cannot import from main
 
# with open("configs/config.toml", "rb") as config:
#     data = tomli.load(config)
#     prefix = data["bot"]["prefix"]
#     administrators = data["bot"]["roles"]["administrators"]
#     moderators = data["bot"]["roles"]["moderators"]
#     owner_id = data["bot"]["ownerID"]
#     footer = data["modules"]["embeds"]["footerCopyright"]
#     footer_img = data["modules"]["embeds"]["footerCopyrightImage"]

# class BotBase(commands.Cog):
#     def __init__(self, bot, intents):
#         self.bot = bot
        
#     intents = discord.Intents.all()
#     bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)
#     staff = administrators + moderators

#     def getConfigValue(self, config_key, key):
#         # check if file exists
#         if not os.path.isfile(f"configs/{config_key}-config.json"):
#             print(f"Nie znaleziono pliku konfiguracyjnego {config_key}-config.json!")
#             # sendError(f"Nie znaleziono pliku konfiguracyjnego {config_key}-config.json!")
#             return False

#         with open(f"configs/{config_key}-config.json", "r") as config: 
#             data = json.load(config)
#             return data[key]

# async def setup(bot):
#     intents = discord.Intents.default()
#     intents.members = True
#     await bot.add_cog(BotBase(bot, intents=intents))