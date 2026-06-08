from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import base64
import time
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

BOT_TOKEN = os.getenv("BOT_TOKEN")
IMGBB_API = os.getenv("IMGBB_API")

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🖼 Image uploader bot\n\n"
        "Reply to any image and use /tgm\n"
        "By - @Naruto_464"
    )
    await update.message.reply_text(text)


# TGM COMMAND
async def tgm(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to an image first.")
        return

    replied = update.message.reply_to_message

    if not replied.photo:
        await update.message.reply_text("❌ Reply to a valid image.")
        return

    msg = await update.message.reply_text("📤 Uploading...")

    start_time = time.time()

    try:
        photo = replied.photo[-1]

        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()

        encoded_image = base64.b64encode(image_bytes).decode()

        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": IMGBB_API,
                "image": encoded_image
            }
        ).json()

        if "data" not in response:
            await msg.edit_text(f"❌ Upload failed\n{response}")
            return

        image_url = response["data"]["url"]
        total_time = round(time.time() - start_time, 2)

        await msg.edit_text(
            f"✅ Uploaded in {total_time}s\n\n{image_url}"
        )

    except Exception as e:
        await msg.edit_text(f"❌ Error:\n{e}")


# APP SETUP
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tgm", tgm))


# 🔴 FAKE WEB SERVER (Render Web Service fix)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()


print("Bot Running...")
app.run_polling()
