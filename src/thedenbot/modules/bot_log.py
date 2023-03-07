from telegram import Update
from telegram.ext import ContextTypes
from logging import getLogger, Formatter
from logging.handlers import TimedRotatingFileHandler


LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
log = None


def get_log(log_path=None):
    log = getLogger(__name__)
    handler = TimedRotatingFileHandler(log_path,
                                       when="d",
                                       interval=1,
                                       backupCount=60)
    formatter = Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


async def bot_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global log
    log_msg = u'#{title} ({type}) [{first_name} ' \
              u'{last_name}] (@{username}) {text}'
    error_msg = u'error parsing message: ({0}) {1}'
    log_path = context.application.bot_data.get('config', {}).get('log_path')
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
