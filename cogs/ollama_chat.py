import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

class OllamaChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Dictionnaire pour stocker la mémoire de chaque utilisateur
        # Format : { "id_utilisateur": [ {"role": "user", "content": "..."}, ... ] }
        self.memory = {}
        self.ollama_url = "http://localhost:11434/api/chat"

    @app_commands.command(name="ia", description="Discute avec l'IA locale Ollama")
    @app_commands.choices(modele=[
        app_commands.Choice(name="Llama 3 (Meta)", value="llama3"),
        app_commands.Choice(name="Mistral (Français optimisé)", value="mistral"),
        app_commands.Choice(name="qwen:0.5b (Léger et rapide)", value="qwen:0.5b"),
        app_commands.Choice(name="deepseek:r1", value="deepseek-r1:7b"),
    ])
    async def chat_ia(self, interaction: discord.Interaction, message: str, modele: app_commands.Choice[str] = None):
        # 1. Indique à Discord que le bot réfléchit (Ollama peut prendre quelques secondes)
        await interaction.response.defer()

        user_id = interaction.user.id
        # Si aucun modèle n'est sélectionné, on prend Llama 3 par défaut
        selected_model = modele.value if modele else "llama3"

        # 2. Initialisation et gestion de la mémoire
        if user_id not in self.memory:
            # On peut ajouter un "System Prompt" caché au début si on veut
            self.memory[user_id] = [
                {"role": "system", "content": "Tu es l'assistant IA personnel du serveur de Mathis. Tu réponds de manière concise et en français."}
            ]

        self.memory[user_id].append({"role": "user", "content": message})

        # Limite de mémoire : on ne garde que les 15 derniers messages pour ne pas faire exploser la RAM
        if len(self.memory[user_id]) > 15:
            # On garde le system prompt (index 0) et les 14 derniers messages
            self.memory[user_id] = [self.memory[user_id][0]] + self.memory[user_id][-14:]

        # 3. Préparation de la requête pour l'API d'Ollama
        payload = {
            "model": selected_model,
            "messages": self.memory[user_id],
            "stream": False # On attend la réponse complète avant d'envoyer
        }

        # 4. Connexion à Ollama et envoi de la réponse
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.ollama_url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        bot_reply = data["message"]["content"]

                        # Ajout de la réponse du bot dans la mémoire
                        self.memory[user_id].append({"role": "assistant", "content": bot_reply})

                        # Découpage si la réponse dépasse la limite de 2000 caractères de Discord
                        if len(bot_reply) > 1950:
                            await interaction.followup.send(f"**Toi:** {message}\n**IA ({selected_model}):**\n{bot_reply[:1950]}...\n*(Réponse tronquée car trop longue)*")
                        else:
                            await interaction.followup.send(f"**Toi:** {message}\n**IA ({selected_model}):**\n{bot_reply}")
                    else:
                        # En cas d'erreur de modèle non trouvé
                        self.memory[user_id].pop() # Annule l'ajout du message utilisateur dans la mémoire
                        await interaction.followup.send(f"❌ Erreur : Le modèle `{selected_model}` n'est pas installé sur ta machine. Tape `ollama pull {selected_model}` dans ton terminal.")

        except aiohttp.ClientConnectorError:
            self.memory[user_id].pop()
            await interaction.followup.send("❌ Impossible de joindre Ollama. L'application Ollama est-elle bien lancée sur ton Mac ?")

    # Commande bonus pour effacer la mémoire manuellement
    @app_commands.command(name="ia_reset", description="Efface ta conversation actuelle avec l'IA")
    async def reset_memory(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in self.memory:
            del self.memory[user_id]
        await interaction.response.send_message("🧹 La mémoire de l'IA a été effacée. On repart de zéro !")

async def setup(bot):
    await bot.add_cog(OllamaChat(bot))
