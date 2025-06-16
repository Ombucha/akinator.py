# pylint: skip-file

import discord
import akinator

from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class AkiView(discord.ui.View):
    def __init__(self, aki, user):
        super().__init__(timeout=120)
        self.aki = aki
        self.user = user
        self.value = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.user

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, row=0)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "yes"
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, row=0)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "no"
        self.stop()

    @discord.ui.button(label="Probably", style=discord.ButtonStyle.blurple, row=1)
    async def probably(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "p"
        self.stop()

    @discord.ui.button(label="Probably Not", style=discord.ButtonStyle.blurple, row=1)
    async def probably_not(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "pn"
        self.stop()

    @discord.ui.button(label="I don't know", style=discord.ButtonStyle.gray, row=1)
    async def idk(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "i"
        self.stop()

    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary, row=2)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "back"
        self.stop()

class GuessView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.user = user
        self.value = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.user

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, row=0)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "yes"
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, row=0)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "no"
        self.stop()

@bot.tree.command(name="akinator", description="Play Akinator in Discord!")
async def akinator_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    aki = akinator.AsyncAkinator()
    await aki.start_game()
    embed = discord.Embed(title="Akinator", description=aki.question, color=discord.Color.blurple())
    embed.set_image(url=aki.akitude_url)
    view = AkiView(aki, interaction.user)
    message = await interaction.edit_original_response(embed=embed, view=view)
    while not aki.finished:
        await view.wait()
        if view.value == "back":
            try:
                await aki.back()
            except akinator.CantGoBackAnyFurther:
                await message.edit(content="You can't go back any further!", embed=None, view=None)
                return
        elif view.value in ["yes", "no", "i", "p", "pn"]:
            try:
                await aki.answer(view.value)
            except akinator.InvalidChoiceError:
                await message.edit(content="Invalid answer. Please try again.", embed=None, view=None)
                return
        else:
            await message.edit(content="Game timed out or cancelled.", embed=None, view=None)
            return
        desc = str(aki)
        embed = discord.Embed(title="Akinator", description=desc, color=discord.Color.blurple())
        embed.set_image(url=aki.akitude_url)
        if desc.strip().lower().startswith("i think of"):
            view = GuessView(interaction.user)
        else:
            view = AkiView(aki, interaction.user)
        await message.edit(embed=embed, view=view)
    result = discord.Embed(title="Akinator's Guess!", color=discord.Color.gold())
    result.add_field(name="Proposition", value=aki.name_proposition or "?", inline=False)
    result.add_field(name="Description", value=aki.description_proposition or "?", inline=False)
    if aki.photo:
        result.set_image(url=aki.photo)
    result.set_footer(text=aki.question)
    await message.edit(embed=result, view=None)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

bot.run('TOKEN')