import json
import discord
import math
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions 

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

class Serverinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command()
    async def serverinfo(self, ctx):
        # role = list(map(lambda r: r.id, ctx.guild.roles))
        # role.pop(0)
        # role = ["<@&" + str(sub) + ">" for sub in role]
        # role2 = ", ".join(role)
        description = f"""**Informacje o Serwerze**
        Emoji - {len(ctx.guild.emojis)}/{ctx.guild.emoji_limit}
        Poziom Boostów - {ctx.guild.premium_tier}
        Liczba Boostów - {ctx.guild.premium_subscription_count} na {len(ctx.guild.premium_subscribers)} boosterów"""
        embed=discord.Embed(title=f"{ctx.guild.name}", description=description, color=0x7289DA, timestamp=ctx.message.created_at)
        embed.add_field(name="ID Serwera", value=ctx.guild.id, inline=True)
        embed.add_field(name="Właściciel", value=f"<@{ctx.guild.owner_id}>", inline=True)
        embed.add_field(name="Region", value=ctx.guild.region, inline=True)
        embed.add_field(name="Założono", value=f"<t:{math.floor(ctx.guild.created_at.timestamp())}>", inline=True)
        embed.add_field(name=f"Liczba Ról", value=f"{len(ctx.guild.roles)}", inline=True)
        embed.add_field(name="Dołączono", value=f"<t:{math.floor(ctx.author.joined_at.timestamp())}>", inline=True)
        embed.add_field(name=f"Kanały tekstowe", value=f"{len(ctx.guild.text_channels)}", inline=True)
        embed.add_field(name="Członkowie", value=ctx.guild.member_count, inline=True)
        embed.add_field(name=f"Kanały Głosowe", value=f"{len(ctx.guild.voice_channels)}", inline=True)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.premium_tier >= 1:
            embed.set_image(url=ctx.guild.banner.url)
        embed.set_footer(text=footer, icon_url=footer_img)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=self.ServerInfoButton())

    class ServerInfoButton(discord.ui.View):
        # primary/blurple = 1
        # secondary/grey/gray = 2
        # success/green = 3
        # danger/red = 4
        # link/url = 5
        @discord.ui.button(label="Lista Ról", style=discord.ButtonStyle.grey)
        async def roles(self, button: discord.ui.Button, interaction: discord.Interaction):
            if button.label == "Lista Ról":
                role = list(map(lambda r: r.id, interaction.message.guild.roles))
                role.pop(0)
                role = ["<@&" + str(sub) + ">" for sub in role]
                role.reverse()
                role2 = "\n".join(role)
                description = f"""**Lista Ról**
                {role2}"""
                embed=discord.Embed(title=f"{interaction.message.guild.name}", description=description, color=0x7289DA, timestamp=interaction.message.created_at)
                embed.set_footer(text=footer, icon_url=footer_img)
                button.label = "Informacje o serwerze"
                await interaction.response.edit_message(view=self, embed=embed)
                return
            if button.label == "Informacje o serwerze":
                description = f"""**Informacje o Serwerze**
                Emoji - {len(interaction.message.guild.emojis)}/{interaction.message.guild.emoji_limit}
                Poziom Boostów - {interaction.message.guild.premium_tier}
                Liczba Boostów - {interaction.message.guild.premium_subscription_count} na {len(interaction.message.guild.premium_subscribers)} boosterów"""
                embed=discord.Embed(title=f"{interaction.message.guild.name}", description=description, color=0x7289DA, timestamp=interaction.message.created_at)
                embed.add_field(name="ID Serwera", value=interaction.message.guild.id, inline=True)
                embed.add_field(name="Właściciel", value=f"<@{interaction.message.guild.owner_id}>", inline=True)
                embed.add_field(name="Region", value=interaction.message.guild.region, inline=True)
                embed.add_field(name="Założono", value=f"<t:{math.floor(interaction.message.guild.created_at.timestamp())}>", inline=True)
                embed.add_field(name=f"Liczba Ról", value=f"{len(interaction.message.guild.roles)}", inline=True)
                embed.add_field(name="Dołączono", value=f"<t:{math.floor(interaction.message.author.joined_at.timestamp())}>", inline=True)
                embed.add_field(name=f"Kanały tekstowe", value=f"{len(interaction.message.guild.text_channels)}", inline=True)
                embed.add_field(name="Członkowie", value=interaction.message.guild.member_count, inline=True)
                embed.add_field(name=f"Kanały Głosowe", value=f"{len(interaction.message.guild.voice_channels)}", inline=True)
                embed.set_thumbnail(url=interaction.message.guild.icon.url)
                if interaction.message.guild.premium_tier >= 1:
                    embed.set_image(url=interaction.message.guild.banner.url)
                embed.set_footer(text=footer, icon_url=footer_img)
                button.label = "Lista Ról"
                # Make sure to update the message with our updated selves
                await interaction.response.edit_message(view=self, embed=embed)
                return

        @discord.ui.button(label="Usuń", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.message.delete()

    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Nie podano wszystkich argumentów!")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

    async def convertSnowflakeToDate(self, snowflake):
        DISCORD_EPOCH = 1420070400000
        #return new Date(snowflake / 4194304 + epoch)
        return math.floor((snowflake / 4194304 + DISCORD_EPOCH) / 1000)

def setup(bot):
    bot.add_cog(Serverinfo(bot))