import discord
from discord import app_commands
from discord.ext import commands

class AdminTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Supprime un certain nombre de messages dans le salon")
    @app_commands.describe(nombre="Nombre de messages à supprimer (max 100)")
    # Optionnel: restreindre cette commande aux administrateurs
    @app_commands.default_permissions(manage_messages=True)
    async def clear_messages(self, interaction: discord.Interaction, nombre: int):
        if nombre < 1 or nombre > 100:
            return await interaction.response.send_message("❌ Choisis un nombre entre 1 et 100.", ephemeral=True)

        await interaction.response.defer(ephemeral=True) # Réponse invisible pour les autres
        deleted = await interaction.channel.purge(limit=nombre)
        await interaction.followup.send(f"🧹 {len(deleted)} messages ont été supprimés !", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminTools(bot))
