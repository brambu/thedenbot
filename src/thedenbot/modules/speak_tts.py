from gtts import gTTS
from tempfile import TemporaryFile
from telegram import Update
from telegram.ext import ContextTypes


async def speak_bot_speak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text = text.removeprefix('/speak ')
    tts = gTTS(text=text, lang='en')
    tmp = TemporaryFile()
    tts.write_to_fp(tmp)
    tmp.seek(0, 0)
    await update.message.reply_audio(
        tmp,
        reply_to_message_id=update.message.message_id,
    )
