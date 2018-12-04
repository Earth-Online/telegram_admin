#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
get some handler
"""
from command import (start, run, add_admin, clearwarns, get_id, admins, get_groups, link, stop, info,
                     globalban, unglobalban, globalban_list, maxwarns, settimeflood, setflood, settings,
                     banword, unbanword, banwords
                     )
from telegram.ext import ConversationHandler, RegexHandler
from message import common_message_handler, telegram_link_handler, limit_set
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
    unglobalban,
    link,
    maxwarns,
    banword,
    unbanword,
    setflood,
    settings,
    settimeflood,
    banwords
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

set_handler = RegexHandler(callback=limit_set, pattern=SETTING_RE, pass_chat_data=True, pass_groups=True)
