#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
from command import start, run, add_admin, clearwarns
from telegram.ext import ConversationHandler
from message import common_message_handler
from constant import RUN

command_handler = [
    start,
    add_admin,
    clearwarns
]

messgae_handler = ConversationHandler(
    entry_points=[run],
    states={
        RUN: [
            common_message_handler
        ],
    },
    fallbacks=[clearwarns]
)

