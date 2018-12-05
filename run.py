#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
run bot
"""
import logging
import pickle
from logging import FileHandler
from telegram.ext import Updater, Dispatcher
from config import LOG_LEVEL, TOKEN, LOG_FILE, CHAT_DATA_FILE, USER_DATA_FILE
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


def loaddata():
    dispatch = Dispatcher.get_instance()
    try:
        with open(CHAT_DATA_FILE, "rb") as f:
            chat_data = pickle.load(f)
            dispatch.chat_data = chat_data
    except FileNotFoundError:
        logging.WARN("chat_data file not found")
    try:
        with open(USER_DATA_FILE, "rb") as f:
            user_data = pickle.load(f)
            dispatch.user_data = user_data
    except FileNotFoundError:
        logging.WARN("user_data file not found")


def main():
    """
    run main function
    """
    updater = Updater(token=TOKEN, request_kwargs={"read_timeout": 30})
    dispatcher = updater.dispatcher
    for command in command_handler:
        logging.debug(f"add {command.command} command")
        dispatcher.add_handler(command)
    dispatcher.add_handler(set_handler)
    dispatcher.add_handler(messgae_handler)

    update_admin_list()
    loaddata()
    logging.info('run bot')
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
