#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
run bot
"""
import logging
import pickle
from logging import FileHandler, StreamHandler
from telegram.ext import Updater, Dispatcher

from command import save_data
from config import LOG_LEVEL, TOKEN, LOG_FILE, CHAT_DATA_FILE, USER_DATA_FILE, DEFAULT_CHECK_TIME, CONV_DATA_FILE
from conversation import conv_handle
from handler import command_handler, set_handler, stop_handler, error_handler, auto_lock_handler, message_handler
from admin import update_admin_list, update_ban_list
from tool import load_jobs
from extra import extra_conv

f_handler = FileHandler(LOG_FILE)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL,
    handlers=[f_handler, StreamHandler()]
)

logger_telegram = logging.getLogger('telegram')
logger_telegram.setLevel(level=logging.WARN)


def loaddata(job_queue):
    dispatch = Dispatcher.get_instance()
    try:
        with open(CHAT_DATA_FILE, "rb") as f:
            chat_data = pickle.load(f)
            dispatch.chat_data = chat_data
    except FileNotFoundError:
        logging.warning("chat_data file not found")
    try:
        with open(USER_DATA_FILE, "rb") as f:
            user_data = pickle.load(f)
            dispatch.user_data = user_data
    except FileNotFoundError:
        logging.warning("user_data file not found")
    try:
        load_jobs(job_queue)
    except FileNotFoundError:
        logging.warning("job_data file not found")
        job_queue.run_repeating(save_data, interval=DEFAULT_CHECK_TIME)


def main():
    """
    run main function
    """
    updater = Updater(token=TOKEN, request_kwargs={"read_timeout": 30}, user_sig_handler=stop_handler)
    dispatcher = updater.dispatcher
    job = updater.job_queue
    for command in command_handler:
        logging.debug(f"add {command.command} command")
        dispatcher.add_handler(command)
    # dispatcher.add_handler(set_handler)
    dispatcher.add_handler(auto_lock_handler)
    dispatcher.add_handler(conv_handle)
    dispatcher.add_handler(extra_conv)
    for message_hand in message_handler:
        dispatcher.add_handler(message_hand)
    dispatcher.add_error_handler(error_handler)

    update_admin_list()
    update_ban_list()
    loaddata(updater.job_queue)
    logging.info('run bot')
    updater.start_polling()
    updater.idle()
    save_data(job=updater.job_queue)


if __name__ == "__main__":
    main()
