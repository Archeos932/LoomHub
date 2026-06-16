import discord
from discord import app_commands
from discord.ext import commands
import os

class Stockage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Remplace par le chemin où tu veux stocker tes fichiers
        self.dossier_stockage = "/Users/mathis/DiscordBox"

        # Le bot crée le dossier tout seul au démarrage s'il n'existe pas
        if not os.path.exists(self.dossier_stockage):
            os.makedirs(self.dossier_stockage)

    @app_commands.command(name="upload", description="Sauvegarde un fichier de Discord vers le Mac")
    @app_commands.describe(fichier="Le fichier à envoyer")
    # Optionnel : réserve cette commande aux admins du serveur
    @app_commands.default_permissions(administrator=True)
    async def save_file(self, interaction: discord.Interaction, fichier: discord.Attachment):
        # Sécurité : on limite à 50 Mo pour éviter de bloquer le bot
        if fichier.size > 50 * 1024 * 1024:
            return await interaction.response.send_message("❌ Fichier trop lourd (Max 50 Mo).", ephemeral=True)

        await interaction.response.defer()

        chemin_complet = os.path.join(self.dossier_stockage, fichier.filename)

        try:
            # La fonction native de discord.py pour télécharger la pièce jointe
            await fichier.save(chemin_complet)
            await interaction.followup.send(f"✅ Fichier `{fichier.filename}` sauvegardé en sécurité sur le Mac !")
        except Exception as e:
            await interaction.followup.send(f"❌ Erreur lors de la sauvegarde : {e}")

async def setup(bot):
    await bot.add_cog(Stockage(bot))
