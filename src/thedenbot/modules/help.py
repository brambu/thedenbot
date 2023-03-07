""" /help command """
from telegram import Update
from telegram.ext import ContextTypes


async def help_command(
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """ example: /help """
    await update.message.reply_text(
        'aroo?',
        reply_to_message_id=update.message.message_id,
    )
