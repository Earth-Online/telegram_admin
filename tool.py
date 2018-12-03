#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
from telegram import Update, Bot
from functools import wraps
from telegram.ext import CommandHandler
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


def check_admin(func):
    @wraps(func)
    def decorator(bot, update, *args, **kwargs):
        """
        :param bot:
        :type bot: Bot
        :param update:
        :type update:Update
        """
        user = update.message.from_user
        if not user_is_admin(user.id):
            # TODO add some error msg
            return
        return func(bot, update, *args, **kwargs)

    return decorator

