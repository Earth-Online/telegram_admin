#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot command
"""
from telegram import Update, Bot, MessageEntity
from telegram.ext import Dispatcher
from constant import START_MSG, ADD_ADMIN_OK_MSG, RUN, ADMIN, BOT_NO_ADMIN_MSG, BOT_IS_ADMIN_MSG
from tool import command_wrap, check_admin
from admin import update_admin_list
from module import DBSession
from module.user import User


@command_wrap()
def start(bot, update):
    """
    send start info
    """
    bot.send_message(chat_id=update.message.chat_id, text=START_MSG)


@command_wrap(name="add")
@check_admin()
def add_admin(bot, update, args):
    """
    add admin
    :param bot:
    :param update:
    :param args:
    :return:
    """
    if not len(args):
        # TODO add msg
        return
    # TODO check id
    session = DBSession()
    for user_id in args:
        user = User(id=user_id, isadmin=True)
        session.merge(user)
    session.commit()
    session.close()
    update_admin_list()
    bot.send_message(id=update.message.chat_id, text=ADD_ADMIN_OK_MSG)


@command_wrap()
@check_admin()
def run(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    bot_id = bot.get_me()['id']
    info = bot.get_chat_member(update.message.chat_id, bot_id)
    if info['status'] == ADMIN:
        bot.send_message(chat_id=update.message.chat_id, text=BOT_NO_ADMIN_MSG)
        return
    bot.send_message(chat_id=update.message.chat_id, text=BOT_IS_ADMIN_MSG)
    return RUN


@command_wrap(pass_args=True)
@check_admin()
def clearwarns(bot, update, args):
    user_list = [args]
    if update.message.reply_to_message:
        user_list.append(update.reply_to_message.from_user['id'])
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == MessageEntity.MENTION:
                user_list.append(entity.user['id'])

    dispatcher = Dispatcher.get_instance()
    user_data = dispatcher.user_data
    for user in user_list:
        user_data[user]['warn'] = 0
