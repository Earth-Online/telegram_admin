#!coding:utf-8
#  Created by bluebird on 2018/12/3
"""
handle massage
"""
import filter
from admin import user_is_ban
from constant import WARN_MSG, SET_OK_MSG, LIMIT_DICT, BanMessageType, RUN, BAN_STATE
from telegram import Update, Bot
from telegram.ext.dispatcher import run_async
from tool import messaage_warp, check_admin, kick_user
from telegram.ext.filters import Filters


@messaage_warp(filters=(filter.TelegramLink() | filter.Lang() | filter.Flood() |
                        filter.Emoji() | filter.Gif() | filter.Numbers()
                        | filter.BanWord() | filter.Lock() | filter.AutoLock()), pass_chat_data=True,
               pass_user_data=True)
@run_async
def telegram_link_handler(bot, update, user_data, chat_data):
    """
    :param chat_data:
    :param user_data:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    update.message.delete()
    warn_user(bot, update, user_data, chat_data)
    return RUN


@messaage_warp(filters=(Filters.all & ~filter.Admin()),
               pass_chat_data=True, pass_user_data=True)
@run_async
def common_message_handler(bot, update, user_data, chat_data):
    """
    :param user_data:
    :param chat_data:
    :param bot:
    :param update:
    :type bot: Bot
    :type update: Update
    :type chat_data:dict
    :type user_data:dict
    :return:
    """
    ban_state = chat_data.get(BAN_STATE, {})
    for ban_type in ban_state.keys():
        if getattr(update.message, ban_type, False):
            update.message.delete()
            warn_user(bot, update, user_data, chat_data)
            return RUN
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type in ban_state.keys():
                update.message.delete()
                warn_user(bot, update, user_data, chat_data)
            return RUN
    if ban_state.get('all'):
        update.message.delete()
        warn_user(bot, update, user_data, chat_data)
        return RUN
    return RUN


@check_admin(admin=True)
@run_async
def limit_set(bot, update, chat_data, groups):
    if not chat_data.get('ban_state'):
        chat_data['ban_state'] = {}

    if LIMIT_DICT.get(groups[0]):
        limits = LIMIT_DICT.get(groups[0])
        for limit in limits:
            if groups[1] == "on":
                if chat_data['ban_state'].get(limit):
                    chat_data['ban_state'].pop(limit)
            else:
                chat_data['ban_state'][limit] = groups[1]
    else:
        if groups[1] == "on":
            if chat_data['ban_state'].get(groups[0]):
                chat_data['ban_state'].pop(groups[0])
        else:
            chat_data['ban_state'][groups[0]] = True
    bot.send_message(update.message.chat_id, text=SET_OK_MSG)
    return RUN


@messaage_warp(filters=filter.NewMember)
@run_async
def new_member(bot, update):
    for members in update.message.new_chat_members:
        if user_is_ban(members.id):
            kick_user(bot=bot, update=update, user_list=[members])
    return RUN


def warn_user(bot, update, user_data, chat_data):
    """

    :param chat_data:
    :param bot:
    :param update:
    :param user_data:
    :type user_data: dict
    :return:
    """
    if chat_data.get(BAN_STATE, {}).get(BanMessageType.WARN) is False:
        bot.send_message(chat_id=update.message.chat_id, text=WARN_MSG)
        user_data['warn'] = user_data.get('warn', 0) + 1
        if chat_data.get('maxwarn'):
            if user_data['warn'] > chat_data.get('maxwarn'):
                kick_user(bot, update, [update.message.from_user.id])
