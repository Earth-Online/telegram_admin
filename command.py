#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot command
"""
from constant import START_MSG
from tool import command_wrap


@command_wrap()
def start(bot, update):
    """
    send start info
    """
    bot.send_message(chat_id=update.message.chat_id, text=START_MSG)
