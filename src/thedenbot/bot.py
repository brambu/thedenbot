#!/usr/bin/env python
'''
.. codeauthor:: brambu
This is a telegram bot
'''

import argparse
import logging
import yaml

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from thedenbot.modules.bot_log import bot_log
from thedenbot.modules.help import help_command
from thedenbot.modules.ping import ping
from thedenbot.modules.speak_tts import speak_bot_speak
from thedenbot.modules.start import start
from thedenbot.modules.weather import weather_get

log = logging.getLogger(__name__)


class Thedenbot(object):
    def __init__(self, config_path=None):
        self.config = None
        self.token = None
        self._load_config(config_path)

    def _load_config(self, config_path):
        config = {}
        with open(config_path) as fh:
            yaml_config = yaml.safe_load(fh)
            config.update(yaml_config)
        try:
            assert config.get('bot_token')
            assert config.get('darksky_token')
            assert config.get('log_path')
        except AssertionError as ex:
            log.warning(u'Configuration error %s %s',
                        type(ex), ex.args)
        self.token = config.get('bot_token')
        del config['bot_token']
        self.config = config

    def run(self):
        command_handlers = {
            'start': start,
            'help': help_command,
            'speak': speak_bot_speak,
            'weather': weather_get,
        }
        text_handlers = [
            ping,
            bot_log,
        ]
        application = Application.builder().token(self.token).build()
        application.bot_data['config'] = self.config
        for command, func in command_handlers.items():
            application.add_handler(CommandHandler(command, func))

        async def root_text_handler(update, context):
            for handler in text_handlers:
                await handler(update, context)

        application.add_handler(
            MessageHandler(filters.TEXT, root_text_handler),
        )
        application.run_polling()


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
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser = setup_parser(parser)
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    bot = Thedenbot(config_path=args.config)
    bot.run()


if __name__ == '__main__':
    main()
