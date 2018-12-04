#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
from command import (start, run, add_admin, clearwarns, get_id, admins, get_groups, link, stop, info,
                     globalban, unglobalban, globalban_list,
                     )
from telegram.ext import ConversationHandler
from message import common_message_handler, telegram_link_handler
from constant import RUN, STOP

command_handler = [
    start,
    add_admin,
    clearwarns,
    get_id,
    admins,
    get_groups,
    info,
    globalban_list,
    globalban,
    unglobalban
]

messgae_handler = ConversationHandler(
    entry_points=[run],
    states={
        RUN: [
            telegram_link_handler,
            common_message_handler,
        ],
        STOP: [

        ]

    },
    fallbacks=[stop]
)

