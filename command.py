#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot command
"""
from constant import START_MSG, ADD_ADMIN_OK_MSG
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
@check_admin
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










