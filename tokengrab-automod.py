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
    # 1 - checks MIMEtype
    if (
        attachment.content_type is not None
        and attachment.content_type.startswith("image/")
    ):
        return True

    # 2 - If badly set MIMEtype, falls back on file extension
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
  # image count is always four. Of coursee, this can be edited if bots decide to adapt, or adopt a new posting pattern, who knows
    if image_count == 4:
        try:
            await message.delete()
        except discord.Forbidden:
            print(
                f"Cannot delete message !"
                f"{message.id} : insufficient permission."
            )
        except discord.HTTPException as exc:
            print(
                f"Discord error thrown while attempting to delete message :"
                f"{message.id} : {exc}"
            )

    await bot.process_commands(message)


bot.run(TOKEN)
