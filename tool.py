#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
import logging
import pickle
from threading import Event
from time import time

from telegram import Update, Bot
from functools import wraps
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.dispatcher import DEFAULT_GROUP
from telegram.utils.promise import Promise

from config import JOB_DATA_FILE
from constant import BAN_STATE
from admin import user_is_admin
from telegram.ext import Dispatcher
from re import compile
from constant import ChatData, NO_RUN_MSG


def command_wrap(name: str = "", pass_chat_data=False, pass_user_data=False, pass_args=False, **kwargs):
    """
    wrap command handle
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            ret = None
            logging.debug(f"call {func.__name__} ")
            try:
                ret = func(*args, **kwargs)
            except Exception as e:
                logging.error(e)
            return ret

        return CommandHandler(name or func.__name__, pass_chat_data=pass_chat_data, pass_user_data=pass_user_data,
                              pass_args=pass_args, callback=wrapper, **kwargs)

    return decorator


def messaage_warp(**kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.debug(f'call {func.__name__}')
            return func(*args, **kwargs)

        return MessageHandler(callback=wrapper, **kwargs)

    return decorator


def check_admin(admin=True):
    def decorator(func):
        @wraps(func)
        def wrapper(bot, update, *args, **kwargs):
            """
            :param bot:
            :type bot: Bot
            :param update:
            :type update:Update
            """
            user = update.message.from_user
            if user_is_admin(user.id) != admin:
                bot.send_message(chat_id=update.message.chat_id, text="انت لست مشرف")
                return
            return func(bot, update, *args, **kwargs)

        return wrapper

    return decorator


def check_run():
    def decorator(func):
        @wraps(func)
        def wrapper(bot, update, *args, **kwargs):
            """
            :param bot:
            :type bot: Bot
            :param update:
            :type update:Update
            """
            chat_data = get_chat_data(update.message.chat_id)
            if not chat_data.get(ChatData.RUN):
                bot.send_message(chat_id=update.message.chat_id, text=NO_RUN_MSG)
                return
            return func(bot, update, *args, **kwargs)

        return wrapper

    return decorator


def check_ban_state(chat_id, key):
    dispatcher = Dispatcher.get_instance()
    chat_data = dispatcher.chat_data[chat_id]
    ban_state = chat_data.get(BAN_STATE, dict())
    return bool(ban_state.get(key, False))


def get_chat_data(chat_id=None) -> dict:
    dispatcher = Dispatcher.get_instance()
    return dispatcher.chat_data[chat_id] if chat_id else dispatcher.chat_data


def get_user_data(user_id=None) -> dict:
    dispatcher: Dispatcher = Dispatcher.get_instance()
    dispatcher.handlers.get(DEFAULT_GROUP)
    return dispatcher.user_data[user_id] if user_id else dispatcher.user_data


def get_conv_data():
    """
    some hack code
    :return:
    """
    dispatcher: Dispatcher = Dispatcher.get_instance()
    handlers = dispatcher.handlers.get(DEFAULT_GROUP)
    for handler in handlers:
        # hard code
        if isinstance(handler, ConversationHandler) and handler.states.get(1):
            resolved = dict()
            for k, v in handler.conversations.items():
                if isinstance(v, tuple) and len(v) is 2 and isinstance(v[1], Promise):
                    try:
                        new_state = v[1].result()  # Result of async function
                    except:
                        new_state = v[0]  # In case async function raised an error, fallback to old state
                    resolved[k] = new_state
                else:
                    resolved[k] = v
            return resolved


def save_jobs(jq):
    if jq:
        job_tuples = jq._queue.queue
    else:
        job_tuples = []

    with open(JOB_DATA_FILE, 'wb') as fp:
        for next_t, job in job_tuples:
            # Back up objects
            _job_queue = job._job_queue
            _remove = job._remove
            _enabled = job._enabled

            # Replace un-pickleable threading primitives
            job._job_queue = None  # Will be reset in jq.put
            job._remove = job.removed  # Convert to boolean
            job._enabled = job.enabled  # Convert to boolean

            # Pickle the job
            pickle.dump((next_t, job), fp)

            # Restore objects
            job._job_queue = _job_queue
            job._remove = _remove
            job._enabled = _enabled


def load_jobs(jq):
    now = time()

    with open(JOB_DATA_FILE, 'rb') as fp:
        while True:
            try:
                next_t, job = pickle.load(fp)
            except EOFError:
                break  # Loaded all job tuples

            # Create threading primitives
            enabled = job._enabled
            removed = job._remove

            job._enabled = Event()
            job._remove = Event()

            if enabled:
                job._enabled.set()

            if removed:
                job._remove.set()

            next_t -= now  # Convert from absolute to relative time

            jq._put(job, next_t)


def word_re(word_list: list):
    re = "|".join(word_list)
    return compile(re)


def kick_user(bot, update, user_list):
    """
    :param user_list:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    """
    for user in user_list:
        bot.kick_chat_member(chat_id=update.message.chat_id, user_id=user)


def time_send_msg(bot, job):
    text = job.context[1]
    bot.send_message(chat_id=job.context[2], text=text)
