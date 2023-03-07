from telegram import Update
from telegram.ext import ContextTypes


async def help_command(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await update.message.reply_text(
        'aroo?',
        reply_to_message_id=update.message.message_id,
    )
