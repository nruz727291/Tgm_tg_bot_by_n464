from telegram import Update
from telegram.ext import (
Application,
CommandHandler,
ContextTypes
)

import requests
import base64
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
IMGBB_API = os.getenv("IMGBB_API")

START COMMAND

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

text = (
    "🖼 Image uploader url bot\n\n"
    "By - @Naruto_464"
)

await update.message.reply_text(text)

TGM COMMAND

async def tgm(update: Update, context: ContextTypes.DEFAULT_TYPE):

if not update.message.reply_to_message:

    await update.message.reply_text(
        "❌ Please reply to an image to generate URL."
    )
    return

replied = update.message.reply_to_message

if not replied.photo:

    await update.message.reply_text(
        "❌ Please reply to a valid image."
    )
    return

msg = await update.message.reply_text(
    "📤 Uploading to ImgBB..."
)

start_time = time.time()

try:

    photo = replied.photo[-1]

    file = await context.bot.get_file(
        photo.file_id
    )

    image_bytes = await file.download_as_bytearray()

    encoded_image = base64.b64encode(
        image_bytes
    )

    response = requests.post(
        "https://api.imgbb.com/1/upload",
        data={
            "key": IMGBB_API,
            "image": encoded_image
        }
    ).json()

    image_url = response["data"]["url"]

    total_time = round(
        time.time() - start_time,
        2
    )

    final_text = (
        f"✅ Uploaded to ImgBB in "
        f"{total_time} seconds.\n\n"
        f"{image_url}"
    )

    await msg.edit_text(final_text)

except Exception as e:

    await msg.edit_text(
        f"❌ Upload failed.\n\n{e}"
    )

app = Application.builder().token(
BOT_TOKEN
).build()

app.add_handler(
CommandHandler("start", start)
)

app.add_handler(
CommandHandler("tgm", tgm)
)

print("Bot Running...")

app.run_polling()
