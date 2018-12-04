#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
from command import start, run, add_admin, clearwarns, get_id, admins, get_groups, link, stop, info
from telegram.ext import ConversationHandler
from message import common_message_handler
from constant import RUN, STOP

command_handler = [
    start,
    add_admin,
    clearwarns,
    get_id,
    admins,
    get_groups,
    info
]

messgae_handler = ConversationHandler(
    entry_points=[run],
    states={
        RUN: [
            link,
            common_message_handler,
        ],
        STOP: [

        ]

    },
    fallbacks=[stop]
)

