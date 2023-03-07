from telegram import Update
from telegram.ext import ContextTypes


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text.startswith("ping!"):
        await update.message.reply_text("pong!", reply_to_message_id=update.message.message_id)
