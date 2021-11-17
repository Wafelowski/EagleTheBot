from datetime import datetime
import os
import discord
import time
import json
from discord.ext import commands
from discord.ext.tasks import loop
from asyncio import sleep



# Get configuration.json
with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    token = data["token"]
    owner_id = data["ownerID"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

if token == "TOKEN":
    print("Błędny token.")
    exit()

def __init__(self, bot):
    self.bot = bot
    self._last_member = None

# Intents
intents = discord.Intents.default()
intents.members = True
# intents = discord.Intents.all()
# The bot
bot = commands.Bot(command_prefix='!', intents = intents)

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"[Cogs] Loaded - {filename[:-3]}")

if __name__ == '__main__':
    for filename in os.listdir("cogs/moderation"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.moderation.{filename[:-3]}")
            print(f"[Cogs - Moderation] Loaded - {filename[:-3]}")

if __name__ == '__main__':
    for filename in os.listdir("cogs/tickets"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.tickets.{filename[:-3]}")
            print(f"[Cogs - Tickets] Loaded - {filename[:-3]}")

if __name__ == '__main__':
    for filename in os.listdir("cogs/util"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.util.{filename[:-3]}")
            print(f"[Cogs - Utilities] Loaded - {filename[:-3]}")
        

# cogss = bot.get_cog('Ban')
# cmds = cogss.get_commands()
# print([c.name for c in cmds])

@loop(seconds=1320)
async def name_change():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="przejazdy alarmowe"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name ="Elektra vs FSV"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name ="PEUP 4.0 | Jutro o 18"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="JaPiotrek"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name ="Elektra GES 110"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="kolumnę OPP"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name ="pałowanie symulator"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name ="AS-420"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name ="prawa autorskie"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="banowanie gier Roblox"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name ="FivePD"))
    await sleep(120)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="przecieki"))
    


@bot.event
async def on_ready():
    print(f"""Zalogowano jako {bot.user}
Discord.py - {discord.__version__}
Bot by Wafelowski.dev""")
    name_change.start()


@bot.listen('on_message')
async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content.startswith("!off"):
                await message.channel.send("Okej")
                exit()
        if message.content.startswith("!ping"):
                before = time.monotonic()
                msg = await message.channel.send("🏓 Pong !")
                ping = (time.monotonic() - before) * 1000
                await msg.edit(content=f"🏓 Pong !  `{int(ping)} ms`")
        if message.content.startswith("!setup") and str(message.author.id) == str(owner_id):
            print("Hell nah")
        

@bot.event
async def when_mentioned(bot, message):
    if message.author.id != bot.user.id:
        await message.channel.send(f"Hej {message.author}, mój prefiks to {prefix}.")

@bot.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
        role = list(map(lambda r: r.id, before.roles))
        role = [str(sub) for sub in role]
        role = ", ".join(role)
        if '842392743287980103' in role:
            new_role = next(role for role in after.roles if role not in before.roles)
            #wspierajacy, sierzant, aspirant, inspektor
            if str(new_role.id) in ('531965941958049833', '788091673384058942', '788092090172440648', '788092207722135562'):
                await after.remove_roles(new_role, reason="Ochrona Anty-Alt")
                channel = bot.get_channel(690185755989114885)
                description = f"""**Zastosowano kontrolę Anty-Alt**
                Użytkownik - <@{after.id}> ({after.id})
                Rola usunięta - <@&{new_role.id}>"""
                embed=discord.Embed(description=description, color=0x2a44ff, timestamp=datetime.now())
                embed.set_author(name="PolishEmergencyV")
                embed.set_thumbnail(url="https://i.imgur.com/0dTPJKT.png")
                embed.set_footer(text=footer, icon_url=footer_img)
                await channel.send(embed=embed)


#@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Witaj {member.mention}.'.format(member))

#@bot.event
async def on_reaction_add(reaction, user):
    channel = bot.get_channel(596428386100838400)
    await channel.send(f'Reakcja - {reaction}. User - {user}')

@bot.event
async def on_command_error(ctx, error):
    channel = bot.get_channel(847040167353122856)
    await channel.send(f"```{ctx}``` \n\n```{error}```") 
    raise error

bot.run(token)