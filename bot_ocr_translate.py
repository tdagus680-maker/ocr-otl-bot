import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PIL import Image
import pytesseract
from transformers import pipeline

# Ambil token dari environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Buat translator model
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-id")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    file_path = "temp.jpg"
    await file.download_to_drive(file_path)

    # OCR: ekstrak teks dari gambar
    text = pytesseract.image_to_string(Image.open(file_path))

    if not text.strip():
        await update.message.reply_text("Aku nggak menemukan teks di gambarnya 🥲")
        return

    # Terjemahkan (EN -> ID)
    result = translator(text[:500])[0]["translation_text"]

    # Balas hasil OCR + terjemahan
    reply = f"📝 *Teks Asli:*\n{text.strip()}\n\n🌍 *Terjemahan (semi-formal):*\n{result}"
    await update.message.reply_text(reply, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Bot berjalan...")
    app.run_polling()
