import discord, datetime, json
from discord.ext import commands
from discord.ext.commands.core import has_permissions

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]
    administrators = data["administrators"]
    moderators = data["moderators"]
    forbidden_roles = data["forbiddenRoles"]
    verif_roles = data["verifRoles"]
    anti_alt_channel = data["antiAltChannel"]

class AntiAlt(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    staff = administrators + moderators

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if verif_roles == [] or forbidden_roles == []:
            return
        if len(before.roles) < len(after.roles):
            before_roles = list(map(lambda r: r.id, before.roles))
            after_roles = list(map(lambda r: r.id, after.roles))

            for role in after.roles:
                if role in before.roles:
                    continue
                if (role.id in forbidden_roles and any(role in before_roles for role in verif_roles)):
                    await after.remove_roles(role, reason="Ochrona Anty-Alt")
                    channel = self.bot.get_channel(anti_alt_channel)
                    description = f"""**Zastosowano kontrolę Anty-Alt**
                    ------------------
                    **Użytkownik**: <@{after.id}> ({after.id})
                    **Rola usunięta** <@&{role.id}>"""
                    embed=discord.Embed(description=description, color=0x2a44ff, timestamp=datetime.datetime.now())
                    embed.set_author(name="Ochrona Anty-Alt")
                    embed.set_thumbnail(url="https://i.imgur.com/0dTPJKT.png")
                    embed.set_footer(text=footer, icon_url=footer_img)
                    await channel.send(embed=embed)


async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(AntiAlt(bot, intents))