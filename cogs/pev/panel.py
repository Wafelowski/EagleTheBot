# import discord, json, requests, tomli
# from discord.ext import commands
# from discord.ext.commands.core import has_permissions
# from utils.functions import modifyConfig
# import urllib

# with open("configs/pevConfig.toml", "rb") as config:
#     data = tomli.load(config)
#     pevmp_api = data["pevmp"]["api"]
    
# with open("configs/config.toml", "rb") as config:
#     data = tomli.load(config)
#     prefix = data["bot"]["prefix"]
#     pevmp_api["token"] = data["api"]["pevmp_api"]
#     pevmp_api["create_key"] = data["api"]["pevmp_api_create_key"]

# class UserPanel(commands.Cog):
#     def __init__(self, bot, intents):
#         self.bot = bot

#     intents = discord.Intents.all()
#     bot = commands.Bot(command_prefix=prefix, intents=intents)

#     def get_user_data(url):
#         """Fetches user data from the provided URL using authorization from config.

#         Args:
#             url: The URL of the API endpoint.

#         Returns:
#             A Python dictionary containing the JSON response from the server,
#             or None if an error occurs.
#         """

#         if not pevmp_api["token"] or pevmp_api["token"] == "":
#             print("No token provided.")
#             return None

#         # Send POST request
#         headers = {
#             'X-Custom-Auth': f'PEVMP-API {pevmp_api["token"]}',
#             # 'Content-Type': 'application/json'
#             'Content-Type': 'application/x-www-form-urlencoded'
#         }

#         parameters = {
#             "token_id": pevmp_api["token_id"],
#             "name": pevmp_api["name"],
#             "filter": "banned='0'",  # Example filter data
#             "limit": "10",  # Example limit
#             "cols": "id, nick, discord, banned"  # Example columns ||| or can be just "*"/"all"/not defined
#         }

#         if pevmp_api["create_token"]: 
#             parameters["tajemnica"] = pevmp_api["create_key"]
#             del parameters["token_id"] # This is due to the fact that the token_id is not needed when creating a new token, and may cause a conflict

#         data_encoded = urllib.parse.urlencode(parameters)

#         parameters = json.dumps(parameters)
#         response = requests.post(url, data=data_encoded, headers=headers)

#         print(response.status_code)
#         # print(response.json())
#         print(response.text)

#         if response.status_code == 200:
#             # return response.json()
#             # if pevmp_api["create_token"]: # BUG Response is as text currently
#                 # modifyConfig("configs/pevConfig.toml", "pevmp", {"token_id": response.["token"]})
#             return "Success!"
#         elif response.status_code == 400:
#             return "400 Bad Request"
#         elif response.status_code == 409:
#             return "409 Conflict, token name might be taken"
#         else:
#             print(f"Error retrieving data: {response.status_code}")
#             return None
        
#     # print(get_user_data("https://pevmp.polishemergencyv.com/api/users.php")) # DEBUG


#     @bot.command()
#     @has_permissions(administrator=True)
#     async def reqtest(self, ctx):
#         print("test")

#         # Make a POST request to a specific website with two parameters in POST body
#         id = 123
#         key = "abc"
#         url = f"https://example.com/"

#         # async with aiohttp.ClientSession() as session:
#         #     async with session.post(url, data={"id": id, "key": key}) as response:
#         #         print(response.status)
#         #         print(await response.text())

#     @reqtest.error
#     async def reqtest_error(self, ctx, error):
#         if isinstance(error, commands.errors.CommandInvokeError):
#             error = error.original
#             raise error
#         # if isinstance(error, commands.errors.MissingRequiredArgument):
#         #     await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}\n```", mention_author=False)
#         elif isinstance(error, commands.errors.MissingPermissions):
#             await ctx.reply("Brak uprawnień!", mention_author=False)
#             raise error
#         else:
#             await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

# async def setup(bot):
#     intents = discord.Intents.default()
#     intents.members = True
#     await bot.add_cog(UserPanel(bot, intents=intents))