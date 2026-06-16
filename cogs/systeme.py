import discord
from discord import app_commands
from discord.ext import commands
import psutil
import time

class Systeme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Affiche la latence du bot")
    async def ping(self, interaction: discord.Interaction):
        # Calcule le temps de réponse de l'API Discord
        latence = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong ! Latence : `{latence}ms`")

    @app_commands.command(name="stats", description="Affiche l'état de la machine hôte")
    async def stats(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # Récupération des données système
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_total = round(ram.total / (1024**3), 1)
        ram_used = round(ram.used / (1024**3), 1)

        # Création d'un bel encadré (Embed) Discord
        embed = discord.Embed(title="📊 État du Serveur", color=discord.Color.blue())
        embed.add_field(name="Processeur (CPU)", value=f"`{cpu_usage}%`", inline=True)
        embed.add_field(name="Mémoire (RAM)", value=f"`{ram_usage}%`\n({ram_used} Go / {ram_total} Go)", inline=True)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Systeme(bot))
