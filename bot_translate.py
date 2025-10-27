import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from transformers import pipeline

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Model terjemahan multilingual (otomatis deteksi bahasa → Indonesia)
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")

def refine_to_semi_formal(text: str) -> str:
    """
    Ubah hasil terjemahan jadi semi-formal (pakai aku–kau, lebih natural)
    """
    replacements = {
        "Anda": "kau",
        "anda": "kau",
        "Kamu": "kau",
        "kamu": "kau",
        "Saya": "Aku",
        "saya": "aku"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    # Terjemahan otomatis → Bahasa Indonesia
    try:
        translation = translator(user_text, src_lang=None, tgt_lang="ind_Latn")[0]["translation_text"]
        refined = refine_to_semi_formal(translation)
        reply = (
            f"📝 *Teks Asli:*\n{user_text}\n\n"
            f"🌍 *Terjemahan (semi-formal):*\n{refined}"
        )
        await update.message.reply_text(reply, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("Maaf, aku lagi kesulitan nerjemahin teks itu 😅")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Bot penerjemah siap berjalan... 🚀")
    app.run_polling()
