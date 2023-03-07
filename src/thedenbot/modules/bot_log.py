""" bot_log handler """
from logging import getLogger, Formatter
from logging.handlers import TimedRotatingFileHandler

from telegram import Update
from telegram.ext import ContextTypes


LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'


def get_log(log_path=None):
    """ configure log for log_path, should only be run once at init """
    log = getLogger(__name__)
    handler = TimedRotatingFileHandler(log_path,
                                       when="d",
                                       interval=1,
                                       backupCount=60)
    formatter = Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


async def bot_log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ listens to all messages with text and logs to file """
    log_msg = '#{title} ({type}) [{first_name} ' \
              '{last_name}] (@{username}) {text}'
    error_msg = 'error parsing message: ({0}) {1}'
    log_path = context.application.bot_data.get('config', {}).get('log_path')
    log = context.application.bot_data.get('log')
    if log is None:
        log = get_log(log_path)
    try:
        log_msg = log_msg.format(
            title=update.message.chat.title,
            type=update.message.chat.type,
            first_name=update.message.from_user.first_name,
            last_name=update.message.from_user.last_name,
            username=update.message.from_user.username,
            text=update.message.text,
        )
    except BaseException as ex:
        log_msg = error_msg.format(ex, vars(update.message.chat))
    log.info(log_msg)
    context.application.bot_data['log'] = log
