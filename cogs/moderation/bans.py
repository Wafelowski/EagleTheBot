import json, discord, re
from discord.ext import commands
from discord.ext.commands.core import has_permissions

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]
    administrators = data["administrators"]
    moderators = data["moderators"]

class Bans(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    staff = administrators + moderators

    @bot.command(aliases=["zbanuj"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(ban_members=True))
    async def ban(self, ctx, member, *, reason = None):
        if ctx.message.mention_everyone:
            await ctx.reply("Na co liczysz?", mention_author=False, delete_after=15.0)
            return
        
        if len(ctx.message.mentions) > 1:
            await ctx.reply(f"Użyj komendy {prefix} jeśli potrzebujesz zbanować kilku użytkowników.", mention_author=False, delete_after=15.0)
            return
        elif len(ctx.message.mentions) == 0:
            member = ctx.guild.get_member(member)
            if member is None:
                await ctx.reply("Nie znaleziono użytkownika.", mention_author=False, delete_after=15.0)
                return
        else:
            member = ctx.message.mentions[0]

        if member.id == ctx.author.id:
            await ctx.send("Dlaczego chcesz zbanować samego siebie?")
            return
        if member.id == self.bot.user.id:
            await ctx.send("Nie mogę zbanować samego siebie.")
            return
        days=0
        daysMsg = ""
        if "-24h" in ctx.message.content:
            days=1
            reason = reason.replace('-24h', '')
            daysMsg = "\nDodatkowo usunięto wiadomości z ostatnich 24 godzin."
        if "-7d" in ctx.message.content:
            days=7
            reason = reason.replace('-7d', '')
            daysMsg = "\nDodatkowo usunięto wiadomości z ostatnich 7 dni."
        silentMsg = "[Flaga -s]"
        if not "-s" in ctx.message.content:
            silentMsg = ""
            description = f"""Otrzymano banicję. Powód: {reason}"""
            embed=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
            embed.set_author(name=ctx.guild.name)
            embed.set_footer(text=footer, icon_url=footer_img)
            await member.send(embed=embed)
        reason = reason.replace('-s', '')
        description = f"""**Nadano banicję.**\n
        **Użytkownik**: <@{member.id}> ({member.name}#{member.discriminator}) 
        **Administrator**: <@{ctx.author.id}> ({ctx.author.id}) 
        **Powód**: {reason} {silentMsg} \n{daysMsg}"""
        embed2=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
        embed2.set_author(name=ctx.guild.name)
        embed2.set_footer(text=footer, icon_url=footer_img)
        try:
            await member.ban(days=days, reason = f"{reason} {silentMsg} {daysMsg}")
        except:
            await ctx.send("Wystąpił błąd. [Bans-53]")
        await ctx.send(embed=embed2)
        

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}ban <@Użytkownik>/ID <powód> (-s) (-24h/-7d) \n```", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

    @bot.command(aliases=["mban"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(ban_members=True))
    async def multiban(self, ctx, *, args):
        reason = None
        if ctx.message.mention_everyone:
            await ctx.reply("Na co liczysz?", mention_author=False, delete_after=15.0)
            return
        
        if len(ctx.message.mentions) == 0:
            ids = []
            reason = [] 
            members = []
            failed = []

            ids = re.findall("[0-9]{17,18}", args)
            reason = [x for x in args.split(" ") if x not in ids]
            reason = " ".join(reason)

            for id in ids:
                if str(id) == str(ctx.author.id):
                    failed.append((id, "Nie możesz zbanować samego siebie"))
                    continue
                elif str(id) == str(self.bot.user.id):
                    failed.append((id, "Podano ID bota"))
                    continue
                    
                member = ctx.guild.get_member(int(id))
                if member != None:
                    members.append(member)
                else:
                    failed.append((id, "Błędne ID"))
        else:
            members = ctx.message.mentions

        print("---------------------")
        print(ids)
        print(members)
        print(reason)

        days=0
        daysMsg = ""
        if "-24h" in ctx.message.content:
            days=1
            reason = reason.replace('-24h', '')
            daysMsg = "\nDodatkowo usunięto wiadomości z ostatnich 24 godzin."
        if "-7d" in ctx.message.content:
            days=7
            reason = reason.replace('-7d', '')
            daysMsg = "\nDodatkowo usunięto wiadomości z ostatnich 7 dni."
        

        for member in members:
            try:
                if member.bot == True:
                    continue
                if not "-s" in ctx.message.content:
                    description = f"""Otrzymano banicję. Powód: {reason}"""
                    dm_embed=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
                    dm_embed.set_author(name=ctx.guild.name)
                    dm_embed.set_footer(text=footer, icon_url=footer_img)
                    await member.send(embed=dm_embed)
                await member.ban(days=days, reason = f"{reason} {silentMsg} {daysMsg}")
            except discord.HTTPException:
                continue
            except Exception as e:
                await ctx.send("Wystąpił błąd. [Bans-155]")
                print(e)
                raise

        print(failed)
            

        silentMsg = "[Flaga -s]"
        if "-s" in ctx.message.content:
            silentMsg = ""
            reason = reason.replace('-s', '')

        members_formatted = []
        for member in members:
            members_formatted.append(f"<@{member.id}> ({member.name}#{member.discriminator})")
        members_formatted = "\n - ".join(members_formatted)

        description = f"""**Nadano banicje.**\n
        **Użytkownicy**: \n - {members_formatted}
        **Administrator**: <@{ctx.author.id}> ({ctx.author.name}#{ctx.author.discriminator}) 
        **Powód**: {reason} {silentMsg} \n{daysMsg}"""
        if failed != []:
            description += "\n**Nieudane:**"
            for fail in failed:
                description += f"\n<@{fail[0]}> - {fail[1]}"
        reply_embed=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
        reply_embed.set_author(name=ctx.guild.name)
        reply_embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.send(embed=reply_embed)
        

    @multiban.error
    async def multiban_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}multiban <@Użytkownicy>/ID <powód> (-s) (-24h/-7d) \n```", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Bans(bot, intents))