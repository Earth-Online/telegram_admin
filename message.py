#!coding:utf-8
#  Created by bluebird on 2018/12/3
"""
handle massage
"""
import filter
from constant import WARN_MSG, SET_OK_MSG, LIMIT_DICT
from telegram import Update, Bot
from tool import messaage_warp, check_admin
from telegram.ext.filters import Filters


@messaage_warp(filters=(filter.TELEGRAM_DOMAIN() | filter.Lang() | filter.Flood() |
                        filter.Lang() | filter.Emoji() | filter.Gif() | filter.Numbers()), pass_chat_data=True,
               pass_user_data=True)
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


@messaage_warp(filters=Filters.all,
               pass_chat_data=True, pass_user_data=True)
@check_admin(admin=False)
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
    ban_state = chat_data.get('ban_state', default=dict())
    for ban_type in ban_state.keys():
        if getattr(update.message, ban_type, False):
            update.message.delete()
            warn_user(bot, update, user_data, chat_data)
            return
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type in ban_state.keys():
                update.message.delete()
                warn_user(bot, update, user_data, chat_data)

            return
    if ban_state.get('all'):
        update.message.delete()
        warn_user(bot, update, user_data, chat_data)
        return


@check_admin(admin=True)
def limit_set(bot, update, chat_data, groups):
    if LIMIT_DICT.get(groups[0]):
        limits = LIMIT_DICT.get(groups[0])
        for limit in limits:
            chat_data['ban_state'][limit] = groups[1]
    else:
        chat_data['ban_state'][groups[0]] = True if groups[1] == "off" else None
    bot.send_message(update.message.chat_id, text=SET_OK_MSG)


def warn_user(bot, update, user_data, chat_data):
    """

    :param chat_data:
    :param bot:
    :param update:
    :param user_data:
    :type user_data: dict
    :return:
    """
    if chat_data.get('warn'):
        bot.send_message(chat_id=update.message.chat_id, text=WARN_MSG)
    user_data['warn'] = user_data.get('warn', default=0) + 1
