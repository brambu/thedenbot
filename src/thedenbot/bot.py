#!/usr/bin/env python
'''
.. codeauthor:: brambu
This is a telegram bot
'''
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler

from telegram import Updater

from .modules.weather import weather_for_zip, \
    weather_print_result
from .modules.gift import gift
from .modules.stock import stock
from .modules.woot import woot


# config
LOG_PATH = '/mnt/brambu_home/telegram_logs/chat_log'
LOG_FORMAT = '%(asctime)s %(name)s [%(levelname)s] %(message)s'
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT)
formatter = logging.Formatter(LOG_FORMAT)
handler = TimedRotatingFileHandler(LOG_PATH,
                                   when="d",
                                   interval=1,
                                   backupCount=60)
handler.setFormatter(formatter)
log.addHandler(handler)


class thedenBot(object):
    def __init__(self, token=None):
        self.token = token
        self.updater = None
        self.dp = None

    @staticmethod
    def start(bot, update):
        bot.sendMessage(update.message.chat_id, text='Bark bark!')

    @staticmethod
    def help_me(bot, update):
        bot.sendMessage(update.message.chat_id, text='*whine?*')

    @staticmethod
    def weather(bot, update):
        zip_code = '10001'
        try:
            zip_code = update.message.text.rsplit('/weather ')[-1]
        except BaseException as ex:
            log.error('Error reading command weather: {0}'.format(ex))
        weather_result = weather_for_zip(zip_code)
        printthis = weather_print_result(weather_result, mode='winter')
        bot.sendMessage(update.message.chat_id, text=printthis)

    @staticmethod
    def stock(bot, update):
        searches = update.message.text.rsplit('/stock ')[-1].rsplit(' ')
        output = stock(searches)
        bot.sendMessage(update.message.chat_id, text=output)

    @staticmethod
    def gift(bot, update):
        bot.sendMessage(update.message.chat_id, text=gift())

    @staticmethod
    def woot(bot, update):
        key = update.message.text.rsplit('/woot ')[-1].rsplit(' ')[0]
        if '/woot' in key:
            key = 'www'
        output = woot(key)
        bot.sendMessage(update.message.chat_id, text=output)

    @staticmethod
    def boterror(bot, update, error):
        bot
        log.warn('Update "%s" caused error "%s"' % (update, error))

    @staticmethod
    def botlog(bot, update):
        bot
        log_msg = "#{title} ({type}) [{first_name} " \
                  "{last_name}] (@{username}) {text}"
        error_msg = 'error parsing message: ({0}) {1}'
        try:
            log_msg = log_msg.format(
                title=update.message.chat.title,
                type=update.message.chat.type,
                first_name=update.message.from_user.first_name,
                last_name=update.message.from_user.last_name,
                username=update.message.from_user.username,
                text=update.message.text
            )
        except BaseException as ex:
            log_msg = error_msg.format(ex, vars(update.message.chat))
        log.info(log_msg)

    def run(self):
        # Create the EventHandler and pass it your bot's token.
        self.updater = Updater(self.token)

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        self.dp.addTelegramCommandHandler("start", self.start)
        self.dp.addTelegramCommandHandler("help", self.help_me)
        self.dp.addTelegramCommandHandler("weather", self.weather)
        self.dp.addTelegramCommandHandler("gift", self.gift)
        self.dp.addTelegramCommandHandler("stock", self.stock)
        self.dp.addTelegramCommandHandler("woot", self.woot)

        # keep an on disk log
        self.dp.addTelegramMessageHandler(self.botlog)

        # log all errors
        self.dp.addErrorHandler(self.boterror)

        # Start the Bot
        self.updater.start_polling()

        self.updater.idle()


def setup_parser(parser):
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='Be verbose.')
    return parser


def main():
    parser = argparse.ArgumentParser()
    parser = setup_parser(parser)
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    bot = thedenBot(
        token='REPLACE_ME_WITH_YOUR_TOKEN'
    )
    bot.run()


if __name__ == '__main__':
    main()
