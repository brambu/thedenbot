""" /start command """
from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """ example: /start """
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_to_message_id=update.message.message_id,
    )
