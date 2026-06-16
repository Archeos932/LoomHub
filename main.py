import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configuration de base (n'oublie pas d'activer les intents sur le portail Discord)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Connecté en tant que {bot.user}')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'📦 Module chargé : {filename}')
            except Exception as e:
                print(f'❌ Erreur de chargement pour {filename}: {e}')

    # AJOUTE CECI : Synchronise les Slash Commands avec Discord
    try:
        synced = await bot.tree.sync()
        print(f"🔄 {len(synced)} commande(s) slash synchronisée(s).")
    except Exception as e:
        print(f"❌ Erreur de synchronisation : {e}")


if __name__ == '__main__':
    bot.run(TOKEN)
