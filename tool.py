#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
import logging
from telegram import Update, Bot
from functools import wraps
from telegram.ext import CommandHandler, MessageHandler
from admin import user_is_admin


def command_wrap(name: str = "", **kwargs):
    """
    wrap command handle
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return CommandHandler(name or func.__name__, wrapper, **kwargs)

    return decorator


def messaage_warp(**kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
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
