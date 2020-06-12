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
from thedenbot.modules.speak_tts import speak_bot_speak

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

    @staticmethod
    def sanitize_msg(msg):
        if msg is None:
            return msg
        if len(msg.split(' ')) < 2:
            return msg
        msg = msg.split('/')[1:]
        msg = '/'.join(msg)
        msg = msg.split(' ')[1:]
        msg = ' '.join(msg)
        return msg

    @staticmethod
    def start(bot, update):
        bot.sendMessage(update.message.chat_id, text='Bark bark!')
        thedenBot.bot_log(bot, update)

    @staticmethod
    def help_me(bot, update):
        bot.sendMessage(update.message.chat_id, text='*whine?*')
        thedenBot.bot_log(bot, update)

    @staticmethod
    def weather(bot, update):
        token = config.get('darksky_token')
        weather_input = 'New York, NY'
        try:
            weather_input = thedenBot.sanitize_msg(update.message.text)
        except BaseException as ex:
            log.error(u'Error reading command weather: %s', ex)
        print_this = weather_get(weather_input, token=token)
        bot.sendMessage(update.message.chat_id, text=print_this)
        thedenBot.bot_log(bot, update)

    @staticmethod
    def stock(bot, update):
        searches = thedenBot.sanitize_msg(update.message.text).split(' ')
        output = stock(searches)
        bot.sendMessage(update.message.chat_id, text=output)
        thedenBot.bot_log(bot, update)

    @staticmethod
    def gift(bot, update):
        bot.sendMessage(update.message.chat_id, text=gift())
        thedenBot.bot_log(bot, update)

    @staticmethod
    def woot(bot, update):
        key = thedenBot.sanitize_msg(update.message.text)
        output = woot(key)
        bot.sendMessage(update.message.chat_id, text=output)
        thedenBot.bot_log(bot, update)

    @staticmethod
    def speak(bot, update, lang='en'):
        msg = thedenBot.sanitize_msg(update.message.text)
        with speak_bot_speak(msg, lang) as fh:
            bot.sendVoice(update.message.chat_id, voice=fh)
        thedenBot.bot_log(bot, update)

    @staticmethod
    def sprechen(bot, update):
        thedenBot.speak(bot, update, lang='de')

    @staticmethod
    def hanashite(bot, update):
        thedenBot.speak(bot, update, lang='ja')

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
        updater = Updater(self.token)

        # on different commands - answer in Telegram
        handlers = {
            'start': self.start,
            'help': self.help_me,
            'weather': self.weather,
            'stock': self.stock,
            'gift': self.gift,
            'woot': self.woot,
            'speak': self.speak,
            'sprechen': self.sprechen,
            'hanashite': self.hanashite,
        }
        for command, callback in handlers.items():
            updater.dispatcher.add_handler(
                CommandHandler(command, callback)
            )

        updater.dispatcher.add_handler(
            MessageHandler(Filters.all, self.bot_log)
        )

        # log all errors
        updater.dispatcher.add_error_handler(self.bot_error)

        # Start the Bot
        updater.start_polling(
            timeout=30,
            read_latency=5,
            bootstrap_retries=3,
            poll_interval=0.3,
        )

        updater.idle()


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
