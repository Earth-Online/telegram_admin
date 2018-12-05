#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
get some handler
"""
import logging
from command import (start, run, add_admin, clearwarns, get_id, admins, get_groups, link, stop, info,
                     globalban, unglobalban, globalban_list, maxwarns, settimeflood, setflood, settings,
                     banword, unbanword, banwords, save, lang, save_data, kick
                     )

from telegram.ext import ConversationHandler, RegexHandler
from message import common_message_handler, telegram_link_handler, limit_set
from constant import RUN, STOP, SETTING_RE

set_handler = RegexHandler(callback=limit_set, pattern=SETTING_RE, pass_chat_data=True, pass_groups=True)

command_handler = [
    start,
    add_admin,
    get_id,
    admins,
    get_groups,
    info,
]

admin_handler = [
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
    banwords,
    save,
    lang,
    clearwarns,
    kick,
    set_handler,
    telegram_link_handler,
    common_message_handler,
]

messgae_handler = ConversationHandler(
    entry_points=[run],
    states={
        RUN: admin_handler,
        STOP: [

        ]

    },
    fallbacks=[stop]
)


def stop_handler(sign, frame):
    save_data()


def error_handler(bot, update, error):
    bot.send_message(chat_id=update.message.chat_id, text="a error")
    logging.error(error)
    return messgae_handler.current_conversation
