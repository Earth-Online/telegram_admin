#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
run bot
"""
import logging
from telegram.ext import Updater
from config import LOG_LEVEL, TOKEN
from handler import command_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL)


def main():
    """
    run main function
    """
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    for command in command_handler:
        dispatcher.add_handler(command)
    updater.start_polling()


if __name__ == "__main__":
    main()
