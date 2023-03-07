""" ping! listener """
from telegram import Update
from telegram.ext import ContextTypes


async def ping(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """ listens to all messages starting with 'ping!' """
    if update.message.text.startswith("ping!"):
        await update.message.reply_text(
            "pong!",
            reply_to_message_id=update.message.message_id,
        )
