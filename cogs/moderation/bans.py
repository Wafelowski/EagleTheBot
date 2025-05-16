import tomli, discord, re, json
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands import MemberConverter

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]
    administrators = data["bot"]["roles"]["administrators"]
    moderators = data["bot"]["roles"]["moderators"]

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
            await ctx.reply(f"Użyj komendy {prefix}multiban jeśli potrzebujesz zbanować kilku użytkowników.", mention_author=False, delete_after=15.0)
            return
        elif len(ctx.message.mentions) == 0:
            converter = MemberConverter()
            member = await converter.convert(ctx, member)
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
            try:
                await member.send(embed=embed)
            except:
                pass

        reason = reason.replace('-s', '')
        description = f"""**Nadano banicję.**\n
        **Użytkownik**: {member.mention} ({member.name}#{member.discriminator})
        **Administrator**: {ctx.author.mention} ({ctx.author.name}#{ctx.author.discriminator})
        **Powód**: {reason} {silentMsg} \n{daysMsg}"""
        embed2=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
        embed2.set_author(name=ctx.guild.name)
        embed2.set_footer(text=footer, icon_url=footer_img)
        try:
            await member.ban(delete_message_days=days, reason = f"{reason} {silentMsg} {daysMsg}")
        except Exception as e:
            await ctx.send(f"Wystąpił błąd. [Bans-53] ```\n{e}\n```")
        await ctx.send(embed=embed2)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}ban <@Użytkowni(-k/-cy)/ID> <powód> (-s) (-24h/-7d) \n```", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

    @bot.command(aliases=["mban"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(ban_members=True))
    async def multiban(self, ctx, *, args):
        reason = None
        failed = []
        if ctx.message.mention_everyone:
            await ctx.reply("Na co liczysz?", mention_author=False, delete_after=15.0)
            return

        if len(ctx.message.mentions) == 0:
            ids = []
            reason = []
            members = []
            

            ids = re.findall("[0-9]{17,19}", args)
            reason = [x for x in args.split(" ") if x not in ids]
            reason = " ".join(reason)

            for id in ids:
                if str(id) == str(ctx.author.id):
                    failed.append((id, "Nie możesz zbanować samego siebie"))
                    continue
                elif str(id) == str(self.bot.user.id):
                    failed.append((id, "Podano ID bota"))
                    continue

                converter = MemberConverter()
                member = await converter.convert(ctx, member)
                bot_member = ctx.guild.get_member(self.bot.user.id)
                if member != None:
                    if member.top_role >= ctx.author.top_role:
                        failed.append((id, "Nie możesz zbanować użytkownika o identycznej hierarchii"))
                        continue
                    elif member.top_role >= bot_member.top_role:
                        failed.append((id, "Bot jest niższy hierarchią"))
                        continue
                    else:
                        members.append(member)
                else:
                    failed.append((id, "Błędne ID/Zbanowane"))
        else:
            members = ctx.message.mentions

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
        if "-s" not in ctx.message.content:
            silentMsg = ""
        else:
            reason = reason.replace('-s', '')

        for member in members:
            try:
                if ("-s" not in ctx.message.content) and (member.bot != True):
                    description = f"""Otrzymano banicję. Powód: {reason}"""
                    dm_embed=discord.Embed(description=description, color=0xff0000, timestamp=ctx.message.created_at)
                    dm_embed.set_author(name=ctx.guild.name)
                    dm_embed.set_footer(text=footer, icon_url=footer_img)
                    try:
                        await member.send(embed=dm_embed)
                    except:
                        pass
                await member.ban(delete_message_days=days, reason = f"{reason} {silentMsg} {daysMsg}")
            except discord.HTTPException as e:
                if e.code == 50013:
                    failed.append((member.id, "Nie można zbanować tego użytkownika, brak uprawnień."))
                continue
            except Exception as e:
                await ctx.send("Wystąpił błąd. [Bans-155]")
                print(e)
                raise

        members_formatted = []
        for member in members:
            members_formatted.append(f"<@{member.id}> ({member.name}#{member.discriminator})")
        members_formatted = "\n - ".join(members_formatted)

        description = f"""**Nadano banicje.**\n
        **Użytkownicy**: \n - {members_formatted}
        **Administrator**: <@{ctx.author.id}> ({ctx.author.name}#{ctx.author.discriminator})
        **Powód**: \n```{reason} {silentMsg} \n{daysMsg}```"""
        if failed != []:
            if members == []:
                description = ""
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

    @bot.command()
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(ban_members=True))
    async def getbans(self, ctx, *, args):
        try:
            server_id = int(args)
            guild = self.bot.get_guild(server_id)

            if guild is None:
                await ctx.send("Guild not found. Please provide a valid server ID.")
                return

            # bans = await guild.bans(limit=2000)
            bans = [entry async for entry in guild.bans(limit=2000)]
            ban_list = []
            for ban_entry in bans:
                ban_list.append({
                    "user_id": ban_entry.user.id,
                    "username": str(ban_entry.user),
                    "reason": ban_entry.reason,
                })

            # Save to a JSON file
            file_name = f"bans_{server_id}.json"
            with open(file_name, "w") as json_file:
                json.dump(ban_list, json_file, indent=4)

            await ctx.reply(content=f"Wyeksportowano {len(ban_list)} banów", file=discord.File(file_name))

        except ValueError:
            await ctx.send("Please provide a valid numeric server ID.")

        except discord.Forbidden:
            await ctx.send("I don't have permission to fetch bans for this server.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Bans(bot, intents))