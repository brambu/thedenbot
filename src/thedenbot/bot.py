#!/usr/bin/env python
'''
.. codeauthor:: brambu
This is a telegram bot
'''
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
import yaml

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from thedenbot.modules.weather import weather_get
from thedenbot.modules.gift import gift
from thedenbot.modules.stock import stock
from thedenbot.modules.woot import woot

# config
LOG_FORMAT = '%(asctime)s %(name)s [%(levelname)s] %(message)s'
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT)
formatter = logging.Formatter(LOG_FORMAT)
config = {}


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
        token = config.get('darksky_token')
        weather_input = 'New York, NY'
        try:
            weather_input = update.message.text.rsplit('/weather ')[-1]
        except BaseException as ex:
            log.error(u'Error reading command weather: %s', ex)
        print_this = weather_get(weather_input, token=token)
        bot.sendMessage(update.message.chat_id, text=print_this)

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
    def bot_error(bot, update, error):
        log.warn(u'%s Update "%s" caused error "%s"', bot, update, error)

    @staticmethod
    def bot_log(bot, update):
        log.debug(u'%s log %s', bot, update)
        log_msg = u'#{title} ({type}) [{first_name} ' \
                  u'{last_name}] (@{username}) {text}'
        error_msg = u'error parsing message: ({0}) {1}'
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
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("help", self.help_me))
        self.dp.add_handler(CommandHandler("weather", self.weather))
        self.dp.add_handler(CommandHandler("gift", self.gift))
        self.dp.add_handler(CommandHandler("stock", self.stock))
        self.dp.add_handler(CommandHandler("woot", self.woot))

        # keep an on disk log
        self.dp.add_handler(MessageHandler(Filters.all, self.bot_log))

        # log all errors
        self.dp.add_error_handler(self.bot_error)

        # Start the Bot
        self.updater.start_polling()

        self.updater.idle()


def setup_parser(parser):
    parser.add_argument('-C', '--config',
                        required=True,
                        help='Specify config file')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='Be verbose.')
    return parser


def main():
    global config
    parser = argparse.ArgumentParser()
    parser = setup_parser(parser)
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    with open(args.config) as fh:
        yaml_config = yaml.safe_load(fh)
        config.update(yaml_config)
    try:
        assert config.get('bot_token')
        assert config.get('darksky_token')
        assert config.get('log_path')
    except AssertionError as ex:
        log.warn(u'Configuration error %s %s',
                 type(ex), ex.args)
    handler = TimedRotatingFileHandler(config.get('log_path'),
                                       when="d",
                                       interval=1,
                                       backupCount=60)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    bot = thedenBot(
        token=config.get('bot_token')
    )
    bot.run()


if __name__ == '__main__':
    main()
