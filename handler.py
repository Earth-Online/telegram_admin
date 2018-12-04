#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
from command import (start, run, add_admin, clearwarns, get_id, admins, get_groups, link, stop, info,
                     globalban, unglobalban, globalban_list,
                     )
from telegram.ext import ConversationHandler, RegexHandler
from message import common_message_handler, telegram_link_handler
from constant import RUN, STOP, SETTING_RE

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

set_handler = RegexHandler(pattern=SETTING_RE, pass_chat_data=True, pass_groups=True)
