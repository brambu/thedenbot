""" /speak command """
from tempfile import TemporaryFile

from gtts import gTTS
from telegram import Update
from telegram.ext import ContextTypes


async def speak_bot_speak(
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """ command ex: /speak I speak like this """
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
