#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot command
"""
from datetime import datetime
import pickle

from telegram import Update, Bot, MessageEntity
from telegram import User as tg_user
from telegram.ext import Dispatcher, ConversationHandler
from telegram.chatmember import ChatMember
from telegram import ParseMode
from telegram import ForceReply
from telegram.ext.filters import Filters
from config import CHAT_DATA_FILE, USER_DATA_FILE, CONV_DATA_FILE
from constant import START_MSG, ADD_ADMIN_OK_MSG, RUN, ADMIN, BOT_NO_ADMIN_MSG, BOT_IS_ADMIN_MSG, ID_MSG, ADMIN_FORMAT, \
    GET_ADMINS_MSG, GROUP_FORMAT, BOT_STOP_MSG, STOP, INFO_MSG, GLOBAL_BAN_FORMAT, NO_GET_USENAME_MSG, MAXWARNS_ERROR, \
    BanMessageType, allow_setting, OK, NO, BANWORD_ERROR, BANWORD_FORMAT, GET_BANWORDS_MSG, SET_OK_MSG, BANWORD_KEY, \
    LANGDATA_KEY, TIME_END, BAN_STATE, START_TIME_MSG, STOP_TIME_MSG, AUTO_LOOK_START, AUTO_LOOK_STOP, UserData, \
    ARG_ERROR_MSG, USERID_ERROR_MSG, RunState, NO_INFO_MSG, NUM_ERROR, ChatData, OpenState, OPITON_ERROR
from telegram.ext.dispatcher import run_async
from tool import command_wrap, check_admin, word_re, get_user_data, get_chat_data, get_conv_data, kick_user, \
    messaage_warp
from admin import update_admin_list, update_ban_list
from module import DBSession
from module.user import User
from module.group import Group


@command_wrap()
@run_async
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
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    session = DBSession()
    for user_id in args:
        if not user_id.isdigit():
            bot.send_message(chat_id=update.message.chat_id, text=USERID_ERROR_MSG)
            return
        user = User(id=user_id, isadmin=True)
        session.merge(user)
    session.commit()
    session.close()
    update_admin_list()
    bot.send_message(chat_id=update.message.chat_id, text=ADD_ADMIN_OK_MSG)


@command_wrap(state=RunState.RUN)
@check_admin()
@run_async
def run(bot, update):
    """Run bot filter function
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    bot_id = bot.id
    group_info = bot.get_chat_member(update.message.chat_id, bot_id)
    if group_info['status'] != ChatMember.ADMINISTRATOR:
        bot.send_message(chat_id=update.message.chat_id, text=BOT_NO_ADMIN_MSG)
        return
    session = DBSession()
    group_link = bot.export_chat_invite_link(chat_id=update.message.chat_id)
    group = Group(id=update.message.chat_id, title=update.message.chat.title, link=group_link)
    session.merge(group)
    session.commit()
    session.close()
    bot.send_message(chat_id=update.message.chat_id, text=BOT_IS_ADMIN_MSG)


@command_wrap(pass_args=True, state=RunState.RUN)
@check_admin()
@run_async
def clearwarns(bot, update, args):
    """
    clearn a user warn
    :param bot:
    :param update:
    :param args:
    :type bot: Bot
    :type update: Update
    :return:
    """
    user_list = []
    for _ in args:
        if _.isdigit():
            user_list.append(tg_user(id=_, first_name="temp", is_bot=False))
    if update.message.reply_to_message:
        user_list.append(update.message.reply_to_message.from_user['id'])
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == MessageEntity.TEXT_MENTION:
                user_list.append(entity.user['id'])
    user_data = get_user_data()
    for user in user_list:
        user_data[user][UserData.WARN] = 0
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap(name='id')
@run_async
def get_id(bot, update):
    """
    get user id
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
@run_async
def admins(bot, update):
    """
    get group admin info
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


@command_wrap(name="groups")
@check_admin()
@run_async
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
        ret_text = ret_text + GROUP_FORMAT.format(group_title=group.title, group_id=group.id,
                                                  group_link=group.link)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text, parse_mode=ParseMode.MARKDOWN)
    session.close()


@command_wrap(state=ConversationHandler.END)
@check_admin()
@run_async
def stop(bot, update):
    """
    Stop bot filer function
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    bot.send_message(chat_id=update.message.chat_id, text=BOT_STOP_MSG)
    # return ConversationHandler.END


@command_wrap(state=RunState.RUN)
@check_admin()
@run_async
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


@command_wrap()
@run_async
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
@run_async
def globalban(bot, update, args):
    """
    globalban a user
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    ban_user_list = []
    for _ in args:
        if _.isdigit():
            ban_user_list.append(tg_user(id=_, first_name="not get", is_bot=False))
    for entity in update.message.parse_entities(MessageEntity.TEXT_MENTION).keys():
        ban_user_list.append(entity.user)
    if not len(ban_user_list):
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    ban_user(user_list=ban_user_list, ban=True)
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)
    update_ban_list()


@command_wrap(pass_args=True)
@check_admin()
@run_async
def unglobalban(bot, update, args):
    """
    cancel a user globalbanr
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    ban_user_list = []
    for _ in args:
        if _.isdigit():
            ban_user_list.append(tg_user(id=_, first_name="not get", username="not get", is_bot=False))
    for entity in update.message.parse_entities(MessageEntity.TEXT_MENTION).keys():
        ban_user_list.append(entity.user)
    if not len(ban_user_list):
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    ban_user(user_list=ban_user_list, ban=False)
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)
    update_ban_list()


@command_wrap()
@check_admin()
@run_async
def globalban_list(bot, update):
    """
    show globalban user list
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
        ret_text = ret_text + GLOBAL_BAN_FORMAT.format(user_name=data.id, user_id=data.id)
    session.close()
    if ret_text == "":
        bot.send_message(chat_id=update.message.chat_id, text=NO_INFO_MSG)
        return
    bot.send_message(chat_id=update.message.chat_id, text=ret_text, parse_mode=ParseMode.MARKDOWN)


@command_wrap(pass_chat_data=True, pass_args=True, state=RunState.RUN)
@check_admin()
@run_async
def maxwarns(bot, update, args, chat_data):
    """
    set maxwarn num
    :param args:
    :param chat_data:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :type chat_data: dict
    :return:
    """
    if len(args) == 0 and chat_data.get(ChatData.MAXWARN):
        chat_data.pop(ChatData.MAXWARN)
        return
    if not args[0].isdigit():
        bot.send_message(update.message.chat_id, text=NUM_ERROR)
    chat_data[ChatData.MAXWARN] = int(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap(pass_chat_data=True, pass_args=True, state=RunState.RUN)
@check_admin()
@run_async
def settimeflood(bot, update, args, chat_data):
    """
    set flood limit time
    :param args:
    :param chat_data:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if len(args) == 0 and chat_data.get(ChatData.FLOOD_TIME):
        chat_data.pop(ChatData.FLOOD_TIME)
        return
    if not args[0].isdigit():
        bot.send_message(update.message.chat_id, text=NUM_ERROR)
    chat_data[ChatData.FLOOD_TIME] = int(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap(pass_chat_data=True, pass_args=True, state=RunState.RUN)
@check_admin()
@run_async
def setflood(bot, update, args, chat_data):
    """
    :param args:
    :param chat_data:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if len(args) == 0 and chat_data.get(ChatData.FLOOD_NUM):
        chat_data.pop(ChatData.FLOOD_NUM)
        return
    if not args[0].isdigit():
        bot.send_message(update.message.chat_id, text=NUM_ERROR)
    chat_data[ChatData.FLOOD_NUM] = int(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap(pass_chat_data=True, state=RunState.RUN)
@check_admin()
@run_async
def settings(bot, update, chat_data):
    """
    show group limit setting
    :param chat_data:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    ret_text = ""
    limit = chat_data.get(BAN_STATE, {})
    for setting in allow_setting:
        ret_text = ret_text + f"{setting}" + (NO if limit.get(setting) else OK) + "\n"
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)


@command_wrap(pass_chat_data=True, pass_args=True, state=RunState.RUN)
@check_admin()
@run_async
def banword(bot, update, args, chat_data):
    """
    set banword
    :param chat_data:
    :type chat_data: dict
    :param args:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if not len(args):
        bot.send_message(chat_id=update.message.chat_id, text=BANWORD_ERROR)
        return
    group_banwords = chat_data.get(ChatData.BANWORD, [])
    group_banwords.extend(args)
    chat_data[ChatData.BANWORD] = group_banwords
    chat_data[ChatData.BANWORD_RE] = word_re(group_banwords)
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap(pass_chat_data=True, pass_args=True, state=RunState.RUN)
@check_admin()
@run_async
def unbanword(bot, update, args, chat_data):
    """
    cancel banword
    :param chat_data:
    :type chat_data: dict
    :param args:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if not len(args):
        bot.send_message(chat_id=update.message.chat_id, text=BANWORD_ERROR)
        return
    group_banwords = chat_data.get(ChatData.BANWORD, [])
    for arg in args:
        try:
            group_banwords.remove(arg)
        except ValueError:
            continue
    chat_data[ChatData.BANWORD] = group_banwords
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)
    if not len(group_banwords):
        chat_data[ChatData.BANWORD_RE] = None
        return
    chat_data[ChatData.BANWORD_RE] = word_re(group_banwords)


@command_wrap(pass_chat_data=True, state=RunState.RUN)
@check_admin()
@run_async
def banwords(bot, update, chat_data):
    """
    show banword list
    :param chat_data:
    :type chat_data: dict
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    group_banwords = chat_data.get(ChatData.BANWORD, [])
    ret_text = ""
    for group_banword in group_banwords:
        ret_text = ret_text + BANWORD_FORMAT.format(word=group_banword)
    ret_text = GET_BANWORDS_MSG.format(banwords=ret_text)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)


@command_wrap(pass_chat_data=True, pass_args=True, state=RunState.RUN)
@check_admin()
@run_async
def lang(bot, update, args, chat_data):
    """
    set lang limit
    :param chat_data:
    :param args:
    :param args:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if len(args) < 2:
        bot.send_message(chat_id=update.message.chat_id, text=BANWORD_ERROR)
        return
    ban_list: list = chat_data.get(ChatData.LANG, [])
    if args[1] == OpenState.CLODE:
        ban_list.append(args[0])
        chat_data[ChatData.LANG] = ban_list
    elif args[1] == OpenState.OPEN:
        if args in ban_list:
            ban_list.remove(args[0])
        chat_data[ChatData.LANG] = ban_list
    else:
        bot.send_message(chat_id=update.message.chat_id, text=OPITON_ERROR)
        return
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap()
@check_admin()
@run_async
def save(bot, update):
    """
    save cache data
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    save_data()
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap(pass_args=True, state=RunState.RUN)
@check_admin()
@run_async
def kick(bot, update, args):
    """
    :param args:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    kick_user_list = []
    for _ in args:
        if _.isdigit():
            kick_user_list.append(int(_))
    if update.message.reply_to_message:
        kick_user_list.append(update.message.reply_to_message.from_user['id'])
    ban_users = update.message.parse_entities(types=MessageEntity.TEXT_MENTION)
    kick_user_list.extend([user.user['id'] for user in ban_users.keys()])
    if not len(kick_user_list):
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    kick_user(bot, update, user_list=kick_user_list)
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap(pass_args=True, pass_chat_data=True, state=RunState.RUN)
@check_admin()
@run_async
def lock(bot, update, args, chat_data):
    """
    :param args:
    :param chat_data:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if not len(args) or not args[0].isdigit():
        bot.send_message(chat_id=update.message.chat_id, text=NUM_ERROR)
        return
    chat_data[ChatData.LOCKTIME] = datetime.now().timestamp() + int(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap(pass_chat_data=True, state=RunState.RUN)
@check_admin()
@run_async
def unlock(bot, update, chat_data):
    """
    :param chat_data:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    chat_data[ChatData.LOCKTIME] = None
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


START_TIME = 999
STOP_TIME = 1000


@command_wrap(state=RunState.START_TIME)
@check_admin()
def autolock(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    update.message.reply_text(text=START_TIME_MSG, reply_markup=ForceReply())


@command_wrap(state=RunState.RUN, pass_chat_data=True)
@check_admin()
def unautolock(bot, update, chat_data):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    chat_data[ChatData.AUTO_LOOK_START] = None
    chat_data[ChatData.AUTO_LOOK_STOP] = None


@command_wrap(state=ConversationHandler.END)
@check_admin()
def cancel(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    pass


@messaage_warp(filters=Filters.all, pass_chat_data=True)
@check_admin()
@run_async
def lockstart(bot, update, chat_data):
    """
    :param chat_data:
    :param update:
    :type update: Update
    :return:
    """
    if not update.message.text:
        update.message.reply_text(text=START_TIME_MSG, reply_markup=ForceReply())
        return START_TIME
    try:
        time = datetime.strptime(update.message.text, "%H:%M")
    except ValueError:
        update.message.reply_text(text=START_TIME_MSG, reply_markup=ForceReply())
        return START_TIME
    chat_data[ChatData.AUTO_LOOK_START] = time
    update.message.reply_text(text=STOP_TIME_MSG, reply_markup=ForceReply())
    return STOP_TIME


@messaage_warp(filters=Filters.all, pass_chat_data=True)
@check_admin()
@run_async
def lockstop(bot, update, chat_data):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if not update.message.text:
        update.message.reply_text(text=START_TIME_MSG, reply_markup=ForceReply())
        return STOP_TIME
    try:
        time = datetime.strptime(update.message.text, "%H:%M")
    except ValueError:
        update.message.reply_text(text=START_TIME_MSG, reply_markup=ForceReply())
        return STOP_TIME
    chat_data[ChatData.AUTO_LOOK_STOP] = time
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)
    return ConversationHandler.END


def save_data(_=None, __=None):
    user_data = get_user_data()
    chat_data = get_chat_data()
    conv_data = get_conv_data()
    with open(CHAT_DATA_FILE, 'wb+') as f:
        pickle.dump(chat_data, f)
    with open(USER_DATA_FILE, 'wb+') as f:
        pickle.dump(user_data, f)
    with open(CONV_DATA_FILE, 'wb+') as f:
        pickle.dump(conv_data, f)


def ban_user(user_list, ban=True):
    session = DBSession()
    for user_data in user_list:
        session.merge(User(id=user_data.id, isban=ban, username=user_data.username))
    session.commit()
    session.close()
