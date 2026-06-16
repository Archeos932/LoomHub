import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio
import time

class YoutubeApp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="youtube", description="Télécharge une vidéo YouTube avec choix de la qualité")
    @app_commands.describe(url="Le lien de la vidéo", qualite="Choisis la résolution maximale")
    @app_commands.choices(qualite=[
        app_commands.Choice(name="🎬 4K (Max)", value="2160"),
        app_commands.Choice(name="📺 1080p (Full HD)", value="1080"),
        app_commands.Choice(name="📱 720p (HD)", value="720"),
        app_commands.Choice(name="🎵 Audio seulement (MP3)", value="audio")
    ])
    async def youtube_dl(self, interaction: discord.Interaction, url: str, qualite: app_commands.Choice[str] = None):
        await interaction.response.send_message("⏳ Préparation du téléchargement...")
        message = await interaction.original_response()

        # Si l'utilisateur ne choisit rien, on prend 1080p par défaut pour éviter de saturer le disque
        choix = qualite.value if qualite else "1080"

        def download_video():
            last_update = time.time()

            def progress_hook(d):
                nonlocal last_update
                if d['status'] == 'downloading':
                    now = time.time()
                    if now - last_update > 3:
                        percent = d.get('_percent_str', '0%').strip()
                        coro = message.edit(content=f"⏳ Téléchargement en cours : {percent}")
                        asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                        last_update = now

            # Configuration dynamique selon le choix
            ydl_opts = {
                'outtmpl': '/Users/mathis/Movies/YOUTUBE_DOWNLOAD/%(title)s.%(ext)s',
                'progress_hooks': [progress_hook],
                'quiet': True,
                'noplaylist': True
            }

            if choix == "audio":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                # [height<=X] signifie : "prends cette qualité ou la meilleure en dessous si elle n'existe pas"
                ydl_opts['format'] = f'bestvideo[height<={choix}][ext=mp4]+bestaudio[ext=m4a]/best[height<={choix}][ext=mp4]/best[height<={choix}]'
                ydl_opts['merge_output_format'] = 'mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        try:
            await asyncio.to_thread(download_video)
            type_dl = "Audio" if choix == "audio" else f"Vidéo {choix}p"
            await message.edit(content=f"✅ Téléchargement terminé ({type_dl}) et sauvegardé dans tes films !")
        except Exception as e:
            await message.edit(content=f"❌ Erreur lors du téléchargement : {str(e)}")

async def setup(bot):
    await bot.add_cog(YoutubeApp(bot))
