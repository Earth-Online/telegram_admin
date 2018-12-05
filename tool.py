#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
import logging
from telegram import Update, Bot
from functools import wraps
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.dispatcher import DEFAULT_GROUP
from telegram.utils.promise import Promise
from constant import RUN, BAN_STATE
from admin import user_is_admin
from telegram.ext import Dispatcher
from re import compile


def command_wrap(name: str = "", state=RUN, pass_chat_data=False, pass_user_data=False, pass_args=False, **kwargs):
    """
    wrap command handle
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            logging.debug(f"call {func.__name__} ")
            try:
                ret = func(*args, **kwargs)
            except Exception as e:
                logging.error(e)
            if state:
                return state
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
                # TODO add some error msg
                bot.send_message(chat_id=update.message.chat_id, text="you not admin")
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
        if isinstance(handler, ConversationHandler):
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
