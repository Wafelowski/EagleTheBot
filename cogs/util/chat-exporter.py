from asyncio import sleep
import discord, io, json, chat_exporter
from discord.ext import commands

with open("configs/config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]
    administrators = data["administrators"]
    moderators = data["moderators"]


class ChatExporter(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    staff = administrators + moderators

    @bot.command(aliases=["transkrypt", "chatexport"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(manage_messages=True))
    @commands.guild_only()
    async def transcript(self, ctx):
        if ctx.channel:
            async with ctx.channel.typing():

                messages = [message async for message in ctx.channel.history(limit=None)]
                members = []
                members2 = []

                for message in messages:
                    if message.author.id not in members:
                        members.append(message.author.id)

                for member in members:
                    member = await ctx.guild.fetch_member(member)
                    members2.append(f"- {member.mention}")

                members2 = str(members2).replace("[", "").replace("]", "").replace("'", "").replace(",", "\n")

                embed=discord.Embed(title=f"{ctx.guild.name}", color=0x7289DA, timestamp=ctx.message.created_at)
                embed.set_author(name=f"Transkrypt - {ctx.channel.name}", icon_url=ctx.guild.icon.url)
                embed.add_field(name="Wygenerowano dla", value=f"{ctx.message.author.mention} ({ctx.author.name}#{ctx.author.discriminator})", inline=False)
                embed.add_field(name=f"Uczestnicy ({len(members)}):", value=members2, inline=True)
                embed.add_field(name="Wiadomości:", value=f"{len(messages)}", inline=True)
                embed.set_footer(text=footer, icon_url=footer_img)
                await ctx.message.delete()

                transcript = await chat_exporter.export(
                    channel = ctx.channel, 
                    military_time = True, 
                    tz_info = 'UTC',
                    bot = self.bot)
                transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"{ctx.channel.name}.html")

            transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{ctx.channel.name}.html",)

            await sleep(2)

            await ctx.send(embed=embed, file=transcript_file)

    @transcript.error
    async def transcript_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Nie podano wszystkich argumentów!")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(ChatExporter(bot, intents=intents))