import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import speech_recognition as sr
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.voice.file_id)
    file_path = "voice.ogg"
    await file.download_to_drive(file_path)

    audio = AudioSegment.from_ogg(file_path)
    wav_path = "voice.wav"
    audio.export(wav_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="fa-IR")
        except sr.UnknownValueError:
            text = "متأسفم، نتونستم صداتو بفهمم."
        except sr.RequestError:
            text = "خطا در ارتباط با سرویس تبدیل صدا به متن."

    await update.message.reply_text(text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))
    app.run_polling()
