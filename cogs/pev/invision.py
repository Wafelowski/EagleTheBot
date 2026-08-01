from datetime import datetime, timezone, date
import json, io, requests
import aiomysql, discord, tomli
from discord.ext import commands
from cogs.pev.pev_db import get_connection, date_cnvrt

# checkuser
import re

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    PREFIX = data["bot"]["prefix"]
    FOOTER = data["modules"]["embeds"]["footerCopyright"]
    FOOTER_IMG = data["modules"]["embeds"]["footerCopyrightImage"]
    ADMINISTRATORS = data["bot"]["roles"]["administrators"]
    MODERATORS = data["bot"]["roles"]["moderators"]
    PEV_API = data["api"]["pev_api"]
    BASE_URL = data["modules"]["pev"]["BASE_URL"]

class Invision(commands.Cog):
    def __init__(self, bot, intents):
        self.BOT = bot

    intents = discord.Intents.all()
    BOT = commands.Bot(command_prefix=PREFIX, intents=intents)
    STAFF = ADMINISTRATORS + MODERATORS

    @BOT.command()
    @commands.check_any(commands.has_any_role(*STAFF), commands.has_guild_permissions(ban_members=True))
    async def checkuser(self, ctx, profile):
        author = ctx.author

        if re.match(r"https?://polishemergencyv\.com/profile/\d+-\w+/", profile):
            profile = profile.split("/")[4] 
        elif re.match(r"^\d+$", profile):
            profile = profile
        else:
            return await ctx.reply(f"Nie podano wszystkich argumentów! \n```{PREFIX}checkuser <profil>\n<profil> - link do profilu lub ID użytkownika znajdujące się w linku\n```", mention_author=False)
        
        print(profile)

        async with ctx.channel.typing():
            # from profile get id, for example "2-wafel"
            id = profile.split("-")[0] if "-" in profile else profile

            DB = await get_connection()

            data = {}

            try:
                async with DB.cursor(aiomysql.DictCursor) as cursor:
                    # ipb_core_members
                    await cursor.execute(
                        """
                        SELECT member_id, name, member_group_id, email, joined, ip_address, 
                            warn_level, warn_lastwarn, restrict_post, msg_count_total, 
                            last_visit, last_activity, mod_posts, temp_ban, members_seo_name, mgroup_others, 
                            pp_main_photo, members_disable_pm 
                        FROM polishxinvision.ipb_core_members 
                        WHERE member_id = %s
                        """,
                        (id,)
                    )
                    result = await cursor.fetchone()
                    if result:
                        result['pp_main_photo'] = f"https://polishemergencyv.com/uploads/{result['pp_main_photo']}"
                    data["member"] = result

                    # ipb_core_members_known_ip_addresses
                    await cursor.execute(
                        """
                        SELECT device_key, ip_address 
                        FROM ipb_core_members_known_ip_addresses 
                        WHERE member_id = %s
                        """,
                        (id,)
                    )
                    results = await cursor.fetchall()

                    data["devices"] = list({r["device_key"] for r in results})
                    data["ip_addresses"] = list({r["ip_address"] for r in results})

                    # check if other users used that ip address
                    temp = ", ".join([f"'{x}'" for x in data["ip_addresses"]])
                    await cursor.execute(
                        f"""
                        SELECT m.member_id,
                            m.name,
                            COUNT(k.ip_address) AS ip_count,
                            GROUP_CONCAT(DISTINCT k.ip_address) AS ip_addresses
                        FROM ipb_core_members_known_ip_addresses k
                        JOIN ipb_core_members m ON m.member_id = k.member_id
                        WHERE k.ip_address IN ({temp})
                        AND k.member_id != '{id}'
                        GROUP BY m.member_id, m.name;
                        """
                    )
                    results = await cursor.fetchall()
                    data["other_users_same_ip"] = {
                        r["name"]: {
                            "member_id": r["member_id"],
                            "count": r["ip_count"],
                            "ip_addresses": r["ip_addresses"].split(",")
                        }
                        for r in results
                    }

                    # check if other users have used the same device
                    temp = ", ".join([f"'{x}'" for x in data["devices"]])
                    await cursor.execute(
                        f"""
                        SELECT m.member_id,
                            m.name,
                            COUNT(k.device_key) AS ip_count,
                            GROUP_CONCAT(DISTINCT k.device_key) AS device_keys
                        FROM ipb_core_members_known_devices k
                        JOIN ipb_core_members m ON m.member_id = k.member_id
                        WHERE k.device_key IN ({temp})
                        AND k.member_id != '{id}'
                        GROUP BY m.member_id, m.name;
                        """
                    )
                    results = await cursor.fetchall()
                    data["other_users_same_device"] = {
                        r["name"]: {
                            "member_id": r["member_id"],
                            "count": r["ip_count"],
                            "device_keys": r["device_keys"].split(",")
                        }
                        for r in results
                    }

                    # ipb_core_login_links -> discord id
                    await cursor.execute(
                        """
                        SELECT token_identifier FROM ipb_core_login_links WHERE token_member = %s
                        """,
                        (id,)
                    )
                    result = await cursor.fetchone()
                    if result:
                        # result can be a list or a single value
                        # save last row as discordid, rest as data['discordids']
                        if isinstance(result, list):
                            discordid = result[-1]["token_identifier"]
                            data["discord_ids"] = [r["token_identifier"] for r in result[:-1]]
                        else:
                            discordid = result["token_identifier"]
                            data["discord_ids"] = [discordid]

                    # # GET /core/members/2
                    # resp = requests.get(
                    #     # f"{BASE_URL}/core/members/{id}",
                    #     f"{BASE_URL}/api/core/hello",
                    #     headers={"Authorization": PEV_API}
                    # )
                    # print("Requesting:", f"{BASE_URL}/api/core/hello")
                    # print({"Authorization": PEV_API})

                    # if resp.status_code == 200:
                    #     member = resp.json()
                    #     data["member_api"] = member
                    # else:
                    #     print("Error:", resp.status_code, resp.text)

            except Exception as e:
                print("Exception occurred:", e)

            
            # pevmp_website
            # TODO: Patreon, flagi
            try:
                data["pevmp_website"] = {}
                async with DB.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(
                        """
                        SELECT * FROM pevmp_website.users WHERE discord = %s
                        """,
                        (discordid)
                    )
                    result = await cursor.fetchone()
                    if result:
                        for key, value in result.items():
                            if isinstance(value, (datetime, date)): result[key] = date_cnvrt(value)
                        data["pevmp_website"]["users"] = result

                    await cursor.execute(
                        """
                        SELECT discord, url, email, patreon_id, status, tier, last_charge, next_charge FROM pevmp_website.users_patreon WHERE discord = %s
                        """,
                        (discordid)
                    )
                    result = await cursor.fetchone()
                    if result:
                        for key, value in result.items():
                            if isinstance(value, (datetime, date)): result[key] = date_cnvrt(value)
                        data["pevmp_website"]["patreon"] = result
                    else: 
                        data["pevmp_website"]["patreon"] = False

                    await cursor.execute(
                        """
                        SELECT discord, url, email, patreon_id, status, tier, last_charge, next_charge FROM pevmp_website.users_patreon_archive WHERE discord = %s
                        """,
                        (discordid)
                    )
                    result = await cursor.fetchone()
                    if result:
                        for key, value in result.items():
                            if isinstance(value, (datetime, date)): result[key] = date_cnvrt(value)
                        data["pevmp_website"]["patreon_archive"] = result
                    else: 
                        data["pevmp_website"]["patreon_archive"] = False

                    await cursor.execute(
                        """
                        SELECT * FROM pevmp_website.users_flags WHERE discord = %s
                        """,
                        (discordid)
                    )
                    result = await cursor.fetchall()
                    if result:
                        for key, value in result.items():
                            if isinstance(value, (datetime, date)): result[key] = date_cnvrt(value)
                        data["pevmp_website"]["users_flags"] = result
                    else: 
                        data["pevmp_website"]["users_flags"] = False

            finally:
                DB.close()
            
            
            # DB.close() # DEBUG

            # Create Embed
            embed=discord.Embed(title=f"User Check", color=discord.Color.random(), timestamp=ctx.message.created_at, url=f"https://polishemergencyv.com/profile/{data['member']['member_id']}-{data['member']['members_seo_name']}")
            embed.add_field(name="--- ***Invision*** ---", value="", inline=False)
            embed.add_field(name="ID", value=f"`{data['member']['member_id']}`", inline=True)
            embed.add_field(name="Nick", value=f"`{data['member']['name']}`", inline=True)
            embed.add_field(name="Email", value=f"`{data['member']['email']}`", inline=True)

            embed.add_field(name="Dołączył", value=f"`{datetime.fromtimestamp(data['member']['joined'], tz=timezone.utc).strftime('%d-%m-%Y %H:%M:%S')}`", inline=True)
            embed.add_field(name="Ostatnia wizyta", value=f"`{datetime.fromtimestamp(data['member']['last_visit'], tz=timezone.utc).strftime('%d-%m-%Y %H:%M:%S')}`", inline=True)
            embed.add_field(name="Ostatnia aktywność", value=f"`{datetime.fromtimestamp(data['member']['last_activity'], tz=timezone.utc).strftime('%d-%m-%Y %H:%M:%S')}`", inline=True)

            embed.add_field(name="Grupa (WIP)", value=f"`{data['member']['member_group_id']}`", inline=True)
            embed.add_field(name="Inne grupy (WIP)", value=f"`{data['member']['mgroup_others']}`", inline=True)
            embed.add_field(name="Liczba pryw. wiadomości", value=f"`{data['member']['msg_count_total']}`", inline=True)

            embed.add_field(name="Ostrzeżenia", value=f"`{data['member']['warn_level']}`" if data['member']['warn_level'] is not None else "`0`", inline=True)
            embed.add_field(name="Ostatnie ostrzeżenie", value=f"`{datetime.fromtimestamp(data['member']['warn_lastwarn'], tz=timezone.utc).strftime('%d-%m-%Y %H:%M:%S')}`" if data['member']['warn_lastwarn'] != 0 else "`Brak`", inline=True)
            embed.add_field(name="Zbanowany tymczasowo", value="`Tak`" if data['member']['temp_ban'] != 0 else "`Nie`", inline=True)

            embed.add_field(name="Zablokowane PM", value="`Tak`" if data['member']['members_disable_pm'] != 0 else "`Nie`", inline=True)
            embed.add_field(name="Ograniczone posty", value="`Tak`" if data['member']['restrict_post'] != 0 else "`Nie`", inline=True)
            embed.add_field(name="Moderowane posty", value="`Tak`" if data['member']['mod_posts'] != 0 else "`Nie`", inline=True)

            if data.get("pevmp_website"):
                description = f"""
                --- ***PEVMP Website*** ---\n
                **ID:** `{data['pevmp_website']['users']['id']}`\n
                **Nick:** `{data['pevmp_website']['users']['nick']}`\n
                **Displayname:** `{data['pevmp_website']['users']['displayname']}`\n
                **Utworzono:** `{data['pevmp_website']['users']['created_date']}`\n
                **Ostatnie logowanie:** `{data['pevmp_website']['users']['login_date']}`\n
                **Zbanowany:** `{'Tak' if data['pevmp_website']['users']['banned'] != 0 else 'Nie'}`\n
                **SteamID:** `{data['pevmp_website']['users']['steamid'] if data['pevmp_website']['users']['steamid'] else "Brak"}`
                """

                if data.get('pevmp_website' or {}).get('patreon'):
                    print(data['pevmp_website']['patreon'])
                    description = f"""{description}
                    **Patreon:** [Profil]({data['pevmp_website']['patreon']['url']}), `{data['pevmp_website']['patreon']['email']}`, ID: `{data['pevmp_website']['patreon']['patreon_id']}`
                    **Status:** `{data['pevmp_website']['patreon']['status']}` - `{data['pevmp_website']['patreon']['tier']}`
                    **Ostatnia płatność:** `{data['pevmp_website']['patreon']['last_charge']}` -> `{data['pevmp_website']['patreon']['next_charge']}`
                """

                if data.get('pevmp_website' or {}).get('patreon_archive'):
                    description = f"""{description}
                    ** - Poprzednie konto Patreon - **
                    **Patreon:** [Profil]({data['pevmp_website']['patreon_archive']['url']}), `{data['pevmp_website']['patreon_archive']['email']}`, ID: `{data['pevmp_website']['patreon_archive']['patreon_id']}`
                    **Status:** `{data['pevmp_website']['patreon_archive']['status']}` - `{data['pevmp_website']['patreon_archive']['tier']}`
                    **Ostatnia płatność:** `{data['pevmp_website']['patreon_archive']['last_charge']}` -> `{data['pevmp_website']['patreon_archive']['next_charge']}`
                """
                
                embed.description = description
                print("Description length - ", len(embed.description))
            else:
                embed.add_field(name="--- ***PEVMP Website*** ---", value="Brak powiązanego konta.", inline=False)


            embed.add_field(name="--- ***Discord*** ---", value="", inline=False)
            embed.add_field(name="Discord ID", value=f"`{discordid if discordid else 'Brak powiązanego Discorda'}`", inline=True)
            if len(data.get("discord_ids")) > 1:
                embed.add_field(name="Inne Discord ID", value=f"`{', '.join(data['discord_ids'])}`", inline=True)

            if data['member'] and data['member']['pp_main_photo']:
                embed.set_thumbnail(url=data['member']['pp_main_photo'])
            embed.set_footer(text=f"{FOOTER} | UWAGA POUFNE!!!", icon_url=FOOTER_IMG)


            # Send JSON file or message if not found
            if data["member"]:
                json_bytes = io.BytesIO(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))
                await ctx.author.send(content="Znaleziono użytkownika.", embed=embed, file=discord.File(json_bytes, filename=f"user_{id}.json"))
                # await ctx.author.send(content="Znaleziono użytkownika.", embed=embed, view=Invision.RemoveEmbed_Button, file=discord.File(json_bytes, filename=f"user_{id}.json"))
            else:
                await ctx.author.send("Nie znaleziono użytkownika.")
                return False

            embed=discord.Embed(title=f"Powiązani użytkownicy na stronie PEV", color=discord.Color.random(), timestamp=ctx.message.created_at, url=f"https://polishemergencyv.com/profile/{data['member']['member_id']}-{data['member']['members_seo_name']}")
            temps = []
            temp = ""
            for user in data["other_users_same_ip"]:
                if len(temp) > 900:
                    temps.append(temp)
                    temp = ""
                temp += f"\n `{user}` (`{data['other_users_same_ip'][user]['member_id']}`): {data['other_users_same_ip'][user]['count']} razy"
            for temp in temps:
                embed.add_field(name="Te same IP", value=temp, inline=False)
            if len(data["other_users_same_ip"]) == 0:
                embed.add_field(name="Te same IP", value="Brak", inline=False)
            
            temps = []
            temp = ""
            for user in data["other_users_same_device"]:
                if len(temp) > 900:
                    temps.append(temp)
                    temp = ""
                temp += f"\n `{user}` (`{data['other_users_same_device'][user]['member_id']}`): {data['other_users_same_device'][user]['count']} razy, urządzenia: {', '.join(data['other_users_same_device'][user]['device_keys'])}"
            for temp in temps:
                embed.add_field(name="Inni użytkownicy z tego samego urządzenia", value=temp, inline=False)
            if len(data["other_users_same_device"]) == 0:
                embed.add_field(name="Inni użytkownicy z tego samego urządzenia", value="Brak", inline=False)
            
            await ctx.author.send(content="Znaleziono użytkownika.", embed=embed)

        await ctx.reply("Sprawdzono, wynik na DM.", mention_author=True)

    @checkuser.error
    async def checkuser_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{PREFIX}checkuser <profil> <treść>\n<profil> - link do profilu lub ID użytkownika znajdujące się w linku\n```", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.reply(f"Komenda jest na cooldownie! Spróbuj ponownie za {round(error.retry_after, 2)} sekund(y).", mention_author=False)
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
    await bot.add_cog(Invision(bot, intents=intents))