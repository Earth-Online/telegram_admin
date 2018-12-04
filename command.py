#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot command
"""
from telegram import Update, Bot, MessageEntity
from telegram import User as tg_user
from telegram.ext import Dispatcher
from telegram.chatmember import ChatMember
from telegram import ParseMode
from constant import START_MSG, ADD_ADMIN_OK_MSG, RUN, ADMIN, BOT_NO_ADMIN_MSG, BOT_IS_ADMIN_MSG, ID_MSG, ADMIN_FORMAT, \
    GET_ADMINS_MSG, GROUP_FORMAT, BOT_STOP_MSG, STOP, INFO_MSG, GLOBAL_BAN_FORMAT, NO_GET_USENAME_MSG
from tool import command_wrap, check_admin
from admin import update_admin_list
from module import DBSession
from module.user import User
from module.group import Group


@command_wrap()
def start(bot, update):
    """
    send start info
    """
    bot.send_message(chat_id=update.message.chat_id, text=START_MSG)


@command_wrap(name="add", pass_args=True)
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
    bot.send_message(chat_id=update.message.chat_id, text=ADD_ADMIN_OK_MSG)


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
    bot_id = bot.id
    info = bot.get_chat_member(update.message.chat_id, bot_id)
    if info['status'] != ChatMember.ADMINISTRATOR:
        bot.send_message(chat_id=update.message.chat_id, text=BOT_NO_ADMIN_MSG)
        return
    session = DBSession()
    group = Group(id=update.message.chat_id, title=update.message.chat.title, link=update.message.chat.invite_link)
    session.merge(group)
    session.commit()
    session.close()
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


@command_wrap(name='id')
def get_id(bot, update):
    """

    :param bot:
    :param update:
    :return:
    """
    bot.send_message(chat_id=update.message.chat_id,
                     text=ID_MSG.format(user_id=update.message.from_user['id'],
                                        group_id=update.message.chat_id
                                        )
                     )


@command_wrap()
def admins(bot, update):
    """

    :param bot:
    :type bot: Bot
    :param update:
    :return:
    """
    admin_list = bot.get_chat_administrators(chat_id=update.message.chat_id)
    createors = ""
    adminors = ""
    for admin in admin_list:
        if admin['status'] == ChatMember.CREATOR:
            createors = createors + ADMIN_FORMAT.format(username=admin.user.full_name, user_id=admin.user.id)
        if admin['status'] == ChatMember.ADMINISTRATOR:
            adminors = adminors + ADMIN_FORMAT.format(username=admin.user.full_name, user_id=admin.user.id)
    bot.send_message(chat_id=update.message.chat_id, text=GET_ADMINS_MSG.format(creators=createors, admins=adminors),
                     parse_mode=ParseMode.MARKDOWN)


@command_wrap()
@check_admin()
def get_groups(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    session = DBSession()
    groups = session.query(Group).all()
    ret_text = ""
    for group in groups:
        info = bot.get_chat(chat_id=group.id)
        ret_text = ret_text + GROUP_FORMAT.format(group_title=info.title, group_id=info.id, group_link=info.invite_link)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text, parse_mode=ParseMode.MARKDOWN)


@command_wrap()
@check_admin
def stop(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    bot.send_message(chat_id=update.message.chat_id, text=BOT_STOP_MSG)
    return STOP


@command_wrap()
@check_admin
def link(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    group_link = bot.export_chat_invite_link(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text=group_link)
    return RUN


@command_wrap()
def info(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    send_user = update.message.from_user
    bot.send_message(chat_id=update.message.chat_id,
                     text=INFO_MSG.format(username=send_user.username, user_id=send_user.id))


@command_wrap(pass_args=True)
@check_admin()
def globalban(bot, update, args):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    ban_user_list = []
    if len(args):
        bot.send_message(chat_id=update.message.chat_id, text=NO_GET_USENAME_MSG)
    for _ in args:
        ban_user_list.append(tg_user(id=_, first_name="not get", is_bot=False))
    ban_user_list = list(args)
    for entity in update.message.parse_entities(MessageEntity.MENTION).keys():
        ban_user_list.append(entity.user)
    ban_user(user_list=ban_user_list, ban=True)


@command_wrap(pass_args=True)
@check_admin()
def unglobalban(bot, update, args):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    ban_user_list = []
    if len(args):
        bot.send_message(chat_id=update.message.chat_id, text=NO_GET_USENAME_MSG)
    for _ in args:
        ban_user_list.append(tg_user(id=_, first_name="not get", is_bot=False))
    ban_user_list = list(args)
    for entity in update.message.parse_entities(MessageEntity.MENTION).keys():
        ban_user_list.append(entity.user)
    ban_user(user_list=ban_user_list, ban=False)


@command_wrap()
@check_admin()
def globalban_list(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    session = DBSession()
    datas = session.query(User).filter_by(isban=True).all()
    ret_text = ""
    for data in datas:
        ret_text = GLOBAL_BAN_FORMAT.format(user_name=data.username, user_id=data.id)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text, parse_mode=ParseMode.MARKDOWN)


def ban_user(user_list, ban=True):
    session = DBSession()
    for user_data in user_list:
        session.merge(User(id=user_data.id, isban=ban, username=user_data.username))
    session.commit()
    session.close()
