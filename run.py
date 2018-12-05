#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
run bot
"""
import logging
from logging import FileHandler
from telegram.ext import Updater
from config import LOG_LEVEL, TOKEN, LOG_FILE
from handler import command_handler, messgae_handler, set_handler
from admin import update_admin_list

f_handler = FileHandler(LOG_FILE)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL,
    handlers=f_handler
)

logger_telegram = logging.getLogger('telegram')
logger_telegram.setLevel(level=Warning)


def main():
    """
    run main function
    """
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    for command in command_handler:
        logging.debug(f"add {command.command} command")
        dispatcher.add_handler(command)
    dispatcher.add_handler(set_handler)
    dispatcher.add_handler(messgae_handler)

    update_admin_list()
    logging.info('run bot')
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
