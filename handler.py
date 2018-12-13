#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
get some handler
"""
import logging
from command import (start, run, add_admin, clearwarns, get_id, admins, get_groups, link, stop, info,
                     globalban, unglobalban, globalban_list, maxwarns, settimeflood, setflood, settings,
                     banword, unbanword, banwords, save, lang, save_data, kick, lock, unlock, autolock,
                     cancel, lockstart, lockstop, setmaxmessage, timer, deletetimer,
                     listtimer, unautolock, ping, help, sudo, vipuser, topuser)

from telegram.ext import ConversationHandler, RegexHandler, MessageHandler
from message import common_message_handler, telegram_link_handler, limit_set, new_member, extra_message_handle
from constant import SETTING_RE, RunState

set_handler = RegexHandler(callback=limit_set, pattern=SETTING_RE, pass_chat_data=True, pass_groups=True)

command_handler = [
    start,
    add_admin,
    get_id,
    admins,
    get_groups,
    info,
    globalban_list,
    globalban,
    unglobalban,
    stop,
    run,
    save,
    link,
    maxwarns,
    banword,
    unbanword,
    setflood,
    settings,
    settimeflood,
    setmaxmessage,
    banwords,
    lang,
    clearwarns,
    kick,
    lock,
    unlock,
    timer,
    unautolock,
    deletetimer,
    listtimer,
    ping,
    help,
    sudo,
    vipuser,
    topuser
]

message_handler = [
    set_handler,
    telegram_link_handler,
    new_member,
    extra_message_handle,
    common_message_handler,
]

auto_lock_handler = ConversationHandler(
    entry_points=[autolock],
    states={
        RunState.START_TIME: [
            lockstart
        ],
        RunState.STOP_TIME: [
            lockstop
        ]
    },
    fallbacks=[cancel]
)


def stop_handler(_, __):
    pass
    # save_data()


def error_handler(bot, update, error):
    if update:
        bot.send_message(chat_id=update.message.chat_id, text="a error")
    logging.error(error)
