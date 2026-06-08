import discord
import random
from discord.ext import commands
from pathlib import Path

TOKEN = ""

description = "tokengrab automod"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
    ".heic",
    ".heif",
    ".avif"
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    
def is_image_attachment(attachment: discord.Attachment) -> bool:
    # 1. Vérification MIME
    if (
        attachment.content_type is not None
        and attachment.content_type.startswith("image/")
    ):
        return True

    # 2. Repli sur l'extension
    extension = Path(attachment.filename).suffix.lower()
    return extension in IMAGE_EXTENSIONS


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    image_count = sum(
        1 for attachment in message.attachments
        if is_image_attachment(attachment)
    )

    if image_count == 4:
        try:
            await message.delete()
        except discord.Forbidden:
            print(
                f"Impossible de supprimer le message "
                f"{message.id} : permissions insuffisantes."
            )
        except discord.HTTPException as exc:
            print(
                f"Erreur Discord lors de la suppression "
                f"du message {message.id} : {exc}"
            )

    await bot.process_commands(message)


bot.run(TOKEN)