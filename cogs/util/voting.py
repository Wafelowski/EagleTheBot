import asyncio, discord, json, tomli
import re
from discord.ext import commands
from pathlib import Path
from datetime import datetime

with open("configs/config.toml", "rb") as config:
    data = tomli.load(config)
    prefix = data["bot"]["prefix"]
    footer = data["modules"]["embeds"]["footerCopyright"]
    footer_img = data["modules"]["embeds"]["footerCopyrightImage"]
    administrators = data["bot"]["roles"]["administrators"]
    moderators = data["bot"]["roles"]["moderators"]


class Voting(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    staff = administrators + moderators


    @bot.group(aliases=["ankieta", "vote", "poll"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(manage_messages=True))
    @commands.guild_only()
    async def glosowanie(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Nie wybrano poprawnej opcji; \n- `setup/ustaw` \n- `results/wyniki` \n- `repost` \n- `list/lista` \n- `stop/zamknij`.")
            return

    #################
    # Komenda Setup #
    #################

    @glosowanie.command(aliases=["ustaw"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(manage_messages=True))
    @commands.guild_only()
    async def setup(self, ctx):
        def basic_check(message: discord.Message):
            return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id and message.content != ""

        bot_msg = await ctx.send(f"Rozpoczęto proces tworzenia ankiety. Możesz anulować w każdym momencie wpisując `anuluj`. \nPodaj nazwę ankiety.")
        try: # wait_for(message-name-without_on)
            reply = await self.bot.wait_for('message', check = basic_check, timeout = 60.0)
        except asyncio.TimeoutError: 
            await ctx.send(f"Nie otrzymano odpowiedzi, anulowano proces tworzenia ankiety.")
            await bot_msg.delete()
            await ctx.message.delete()
            return
        
        if reply.content.lower() == "anuluj":
            await ctx.send(f"Anulowano proces tworzenia ankiety.")
            await reply.delete()
            await bot_msg.delete()
            await ctx.message.delete()
            return

        title = reply.content
        embed=discord.Embed(title=title, color=0x7289DA, timestamp=ctx.message.created_at)
        await bot_msg.delete()
        await reply.delete()
        
        bot_msg = await ctx.send(f"Podaj opis ankiety lub wpisz `brak` aby pominąć.")
        try:
            reply = await self.bot.wait_for('message', check = basic_check, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Nie otrzymano odpowiedzi, anulowano proces tworzenia ankiety.")
            await bot_msg.delete()
            await ctx.message.delete()
            return

        if reply.content.lower() == "anuluj":
            await ctx.send(f"Anulowano proces tworzenia ankiety.")
            await reply.delete()
            await bot_msg.delete()
            await ctx.message.delete()
            return

        if reply.content.lower() != "brak":
            description = reply.content
            embed.description = description
        else:
            description = ""

        await bot_msg.delete()
        await reply.delete()

        bot_msg = await ctx.send(f"Podaj kanał, na którym ma zostać opublikowana ankieta.")
        try:
            reply = await self.bot.wait_for('message', check = basic_check, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Nie otrzymano odpowiedzi, anulowano proces tworzenia ankiety.")
            await bot_msg.delete()
            await ctx.message.delete()
            return

        if reply.content.lower() == "anuluj":
            await ctx.send(f"Anulowano proces tworzenia ankiety.")
            await reply.delete()
            await bot_msg.delete()
            await ctx.message.delete()
            return
        
        channel = reply.channel_mentions[0]
        if channel is None:
            channel = ctx.guild.get_channel(int(reply.content))
            if channel is None:
                await ctx.send(f"Kanał nie istnieje lub jest niewidoczny dla bota, anulowano proces tworzenia ankiety.")
                await reply.delete()
                await bot_msg.delete()
                await ctx.message.delete()
                return

        await bot_msg.delete()
        await reply.delete()

        #bot_msg = await ctx.send(f"Podaj datę zakończenia ankiety w formacie `DD-MM-RRRR` lub wpisz `brak` aby pominąć:")
        bot_msg = await ctx.send(f"Podaj dostępne opcje ankiety (oddzielone znakiem `&`). Możesz podać również link do którego będzie przenosiła nazwa opcji, `[nazwa](link)`.")
        try:
            reply = await self.bot.wait_for('message', check = basic_check, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Nie otrzymano odpowiedzi, anulowano proces tworzenia ankiety.")
            await bot_msg.delete()
            await ctx.message.delete()
            return

        if reply.content.lower() == "anuluj":
            await ctx.send(f"Anulowano proces tworzenia ankiety.")
            await reply.delete()
            await bot_msg.delete()
            await ctx.message.delete()
            return

        options = reply.content.split("&")
        if len(options) > 25:
            await ctx.send(f"Lista opcji jest większa niż 25, anulowano proces tworzenia ankiety.")
            await reply.delete()
            await bot_msg.delete()
            await ctx.message.delete()
            return

        for option in options:
            if re.search("\[.*\]\(.*\)", option):
                url = option
                label = option.replace("]", "").replace("[", "").split("(")[0]
                options[options.index(option)] = [label, url]
            else:
                options[options.index(option)] = [option, option]

        await bot_msg.delete()
        await reply.delete()

        # :one: :two: :three: :four: :five: :six: :seven: :eight: :nine: :keycap_ten:

        for index, option in enumerate(options):
            embed.add_field(name=f"Nr. {index}", value=f"{option[1]} \nGłosy - `0`", inline=True)

        vote_id = datetime.now().strftime("%d%m%Y%H%M%S")
        embed.set_footer(text=f"{footer} | Ankieta: {vote_id}", icon_url=footer_img)

        await ctx.send(f"Ankieta została utworzona pomyślnie.", delete_after=30)
        await ctx.message.delete()
        bot_msg = await channel.send(embed=embed, view=Voting.VotingView(ctx, options, vote_id, self.bot))
        self.bot.add_view(Voting.VotingView(ctx, options, vote_id, self.bot))

        with open(f"db/vote_{vote_id}.json", "w") as file:
            votes = []
            users = []
            for index, option in enumerate(options):
                votes.append([index, 0])
            data = {"message_id": bot_msg.id, "vote_id": vote_id, "title": title, "description": description, "channel": channel.id, "options": options, "votes": votes, "users": users}
            json.dump(obj=data, fp=file, ensure_ascii=True, indent=4)
        
    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}patreoncleanup confirm\n```", mention_author=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Brak uprawnień!", mention_author=False)
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

    async def updateVotes(self, vote_id, vote_index, user_id, bot):
        vote_index = int(vote_index[0])
        if not Path(f"db/vote_{vote_id}.json").is_file():
            return False
        with open(f"db/vote_{vote_id}.json", "r") as file:
            data = json.load(file)
            data["votes"][vote_index][1] += 1
            users = data["users"]
            user = [index for (index, user) in enumerate(users) if user[0] == user_id]
            if user != []:
                data["votes"][users[int(str(user).replace("[", "").replace("]", ""))][1]][1] -= 1
                old_vote_index = data["users"][user[0]][1]
                users[user[0]][1] = vote_index
            else:
                old_vote_index = None
                users.append([user_id, vote_index])
        with open(f"db/vote_{vote_id}.json", "w") as file:
            json.dump(obj=data, fp=file, ensure_ascii=False, indent=4)

        await asyncio.sleep(2)

        message = await bot.get_channel(data["channel"]).fetch_message(data["message_id"])
        embed = message.embeds[0]
        if old_vote_index is not None:
            embed.set_field_at(index=old_vote_index, name=f"Nr. {old_vote_index}", value=f"{data['options'][old_vote_index][1]} \nGłosy - `{data['votes'][old_vote_index][1]}`", inline=True)
        embed.set_field_at(index=vote_index, name=f"Nr. {vote_index}", value=f"{data['options'][vote_index][1]} \nGłosy - `{data['votes'][vote_index][1]}`", inline=True)
        await message.edit(embed=embed)

        if old_vote_index != None:
            return f"Zmieniono głos na numer {vote_index}!"
        else:
            return f"Oddano głos na numer {vote_index}!"

        # update embed with rate limit maybe?
        # możliwość włączenia wielu wyborów?


    class VoteButton(discord.ui.Button):
        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer()
            label_index = [index for (index, option) in enumerate(self.view.options) if option[0] == self.label] # self.view.options.index(self.label)
            await interaction.followup.send(await Voting.updateVotes(self, self.view.vote_id, label_index, interaction.user.id, self.view.bot), ephemeral=True)

    class VotingView(discord.ui.View):
        def __init__(self, ctx, options, vote_id, bot):
            super().__init__(timeout=None)
            self.ctx = ctx
            self.options = options
            self.vote_id = vote_id
            self.bot = bot

            for index, option in enumerate(self.options):
                button = Voting.VoteButton(label=option[0], style=discord.ButtonStyle.blurple, custom_id=f"votingview:{index}")
                self.add_item(button)

                
    ###################
    # Komenda Results #
    ###################

    @glosowanie.command(aliases=["wyniki"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(manage_messages=True))
    @commands.guild_only()
    async def results(self, ctx, vote_id):
        try: 
            vote_id = int(vote_id)
        except ValueError:
            await ctx.reply("Podano nieprawidłowy ID ankiety!", mention_author=False)
            return

        if not Path(f"db/vote_{vote_id}.json").is_file():
            await ctx.reply("Nie znaleziono ankiety o podanym ID!", mention_author=False)
            return

        with open(f"db/vote_{vote_id}.json", "r") as file:
            data = json.load(file)
            message_id = data["message_id"]
            title = data["title"]
            description = data["description"]
            channel = data["channel"]
            options = data["options"]
            votes = data["votes"]
            users = data["users"]

        
        def basic_check(message: discord.Message):
            return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id and message.content != ""

        bot_msg = await ctx.send(f"Czy wyniki ankiety mają być anonimowe? (`Tak`/`Nie`)")
        try:
            reply = await self.bot.wait_for('message', check = basic_check, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Nie otrzymano odpowiedzi, anulowano proces tworzenia ankiety.")
            await bot_msg.delete()
            await ctx.message.delete()
            return

        vote_message = await self.bot.get_channel(channel).fetch_message(message_id)

        if vote_message == None:
            vote_message.jump_url = ""

        embed=discord.Embed(title="Kliknij by przejść do ankiety", description=description, url=vote_message.jump_url, color=0x7289DA, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Wyniki | {title}")
        embed.set_footer(text=f"{footer} | Ankieta: {vote_id}", icon_url=footer_img)

        for index, option in enumerate(options):
            embed.add_field(name=f"Nr. {index}", value=f"{option[1]} \nGłosy - `{votes[index][1]}`", inline=True)
        
        if reply.content.lower() == "nie":
            await ctx.send(embed=embed, view=Voting.UsersView(ctx, data, self.bot))
            self.bot.add_view(Voting.UsersView(ctx, data, self.bot))
        else:
            await ctx.send(embed=embed)

        await reply.delete()
        await bot_msg.delete()
        await ctx.message.delete()

    @results.error
    async def results_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}results/wyniki <ID Ankiety>\n```", mention_author=False)
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

    class UsersView(discord.ui.View):
        def __init__(self, ctx, data, bot):
            super().__init__(timeout=None)
            self.ctx = ctx
            self.data = data
            self.bot = bot

        @discord.ui.button(label="Lista Głosujących", style=discord.ButtonStyle.gray, custom_id="users_view:users")
        async def users_list(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()

            message_id = self.data["message_id"]
            vote_id = self.data["vote_id"]
            title = self.data["title"]
            description = self.data["description"]
            channel = self.data["channel"]
            options = self.data["options"]
            votes = self.data["votes"]
            users = self.data["users"]

            vote_message = await self.bot.get_channel(channel).fetch_message(message_id)
            if vote_message == None:
                vote_message.jump_url = ""


            embed=discord.Embed(title="Kliknij by przejść do ankiety", description=description, url=vote_message.jump_url, color=0x7289DA, timestamp=interaction.message.created_at)
            embed.set_author(name=title)
            for index, option in enumerate(options):
                voters = ""
                for user in users:
                    if user[1] == index:
                        voters += f"<@{user[0]}>\n"
                    if len(voters) >= 1000:
                        voters += "..."
                        break
                if voters == "":
                    voters = "Brak głosów"
                embed.add_field(name=f"{option[0]}", value=f"{voters}", inline=True)
            embed.set_footer(text=f"{footer} | Ankieta: {vote_id}", icon_url=footer_img)
            await interaction.followup.send(embed=embed, ephemeral=True)


    ##################
    # Komenda Repost #
    ##################

    @glosowanie.command()
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(manage_messages=True))
    @commands.guild_only()
    async def repost(self, ctx, vote_id):
        try: 
            vote_id = int(vote_id)
        except ValueError:
            await ctx.reply("Podano nieprawidłowy ID ankiety!", mention_author=False)
            return

        if not Path(f"db/vote_{vote_id}.json").is_file():
            await ctx.reply("Nie znaleziono ankiety o podanym ID!", mention_author=False)
            return

        with open(f"db/vote_{vote_id}.json", "r") as file:
            data = json.load(file)
            title = data["title"]
            description = data["description"]
            options = data["options"]
            votes = data["votes"]

        if ctx.message.channel_mentions:
            channel = ctx.message.channel_mentions[0]
        else:
            channel = ctx.message.channel

        embed=discord.Embed(title=title, description=description, color=0x7289DA, timestamp=ctx.message.created_at)

        for index, option in enumerate(options):
            embed.add_field(name=f"Nr. {index}", value=f"{option[1]} \nGłosy - `{votes[index][1]}`", inline=True)
        embed.set_footer(text=f"{footer} | Ankieta: {vote_id}", icon_url=footer_img)

        bot_msg = await channel.send(embed=embed, view=Voting.VotingView(ctx, options, vote_id, self.bot))

        with open(f"db/vote_{vote_id}.json", "w") as file:
            data["message_id"] = bot_msg.id
            json.dump(obj=data, fp=file, ensure_ascii=False, indent=4)

        await ctx.message.delete()

    @repost.error
    async def repost_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Nie podano wszystkich argumentów! \n```{prefix}repost <ID Ankiety> (Kanał)\n```", mention_author=False)
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

    ################
    # Komenda Stop #
    ################

    @glosowanie.command(aliases=["zamknij", "zakończ", "zakoncz"])
    @commands.check_any(commands.has_any_role(*staff), commands.has_guild_permissions(manage_messages=True))
    @commands.guild_only()
    async def stop(self, ctx, vote_id):
        try: 
            vote_id = int(vote_id)
        except ValueError:
            await ctx.reply("Podano nieprawidłowy ID ankiety!", mention_author=False)
            return

        if not Path(f"db/vote_{vote_id}.json").is_file():
            await ctx.reply("Nie znaleziono ankiety o podanym ID!", mention_author=False)
            return

        with open(f"db/vote_{vote_id}.json", "r") as file:
            data = json.load(file)
            message_id = data["message_id"]
            channel = data["channel"]

        vote_message = await self.bot.get_channel(channel).fetch_message(message_id)
        if vote_message == None:
            await ctx.reply("Nie znaleziono wiadomości z ankietą!", mention_author=False)
            return

        embed = vote_message.embeds[0]
        await vote_message.edit(embed=embed, view=Voting.StopVoteView(ctx))

    class StopVoteView(discord.ui.View):
        def __init__(self, ctx):
            super().__init__(timeout=None)
            self.ctx = ctx

        @discord.ui.button(label="Głosowanie zakończone", style=discord.ButtonStyle.gray, disabled=True)
        async def vote_stopped(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Głosowanie zostało zakończone!", ephemeral=True)
        



async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Voting(bot, intents=intents))

    # Persistent views potrzebują parametrów?
    # jak to kurwa działa?