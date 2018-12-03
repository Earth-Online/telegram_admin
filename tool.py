#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
from telegram.ext import CommandHandler

def command_wrap(name: str = "", **kwargs):
    """
    wrap command handle
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return CommandHandler(name or func.__name__, wrapper, **kwargs)
    return decorator

