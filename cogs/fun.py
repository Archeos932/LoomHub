import discord
from discord import app_commands
from discord.ext import commands
import random

class FunTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pile_ou_face", description="Lance une pièce")
    async def coin_flip(self, interaction: discord.Interaction):
        resultat = random.choice(["Pile", "Face"])
        await interaction.response.send_message(f"🪙 La pièce tourne... et c'est **{resultat}** !")

    @app_commands.command(name="choix", description="Le bot choisit entre plusieurs options pour toi")
    @app_commands.describe(options="Sépare tes choix par des virgules (ex: Pizza, Sushi, Burger)")
    async def random_choice(self, interaction: discord.Interaction, options: str):
        liste_choix = [choix.strip() for choix in options.split(",")]

        if len(liste_choix) < 2:
            return await interaction.response.send_message("❌ Il me faut au moins 2 options séparées par des virgules !")

        choix_gagnant = random.choice(liste_choix)
        await interaction.response.send_message(f"🤔 J'ai réfléchi, et je te conseille : **{choix_gagnant}**")

async def setup(bot):
    await bot.add_cog(FunTools(bot))
