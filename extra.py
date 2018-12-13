#!coding:utf-8
#  Created by bluebird on 2018/12/13
"""
docs
"""
from telegram.ext import run_async, Filters, ConversationHandler

from constant import EXTRA_MSG, RunState, EXTRA_EXIT_MSG, EXTRA_SAVE_MSG, UserData, ChatData
from tool import command_wrap, check_admin, messaage_warp, get_chat_data


@command_wrap()
@check_admin()
@run_async
def extra(bot, update):
    update.message.reply_text(text=EXTRA_MSG)
    return RunState.EXTRA_START


@messaage_warp(filters=Filters.all, pass_user_data=True)
def extra_start(bot, update, user_data):
    user_data[UserData.TMP] = update.message.text
    update.message.reply_text(text=EXTRA_EXIT_MSG)
    return RunState.EXTRA_EXIT


@messaage_warp(filters=Filters.all, pass_user_data=True)
def extra_exit(bot, update, user_data):
    chat_data = get_chat_data()
    tmp = chat_data.get(ChatData.EXTRA, {})
    tmp[user_data[UserData.TMP]] = update.message.text
    chat_data[ChatData.EXTRA] = tmp
    update.message.reply_text(text=EXTRA_SAVE_MSG)
    return ConversationHandler.END


@command_wrap(name="الغاء")
@check_admin()
def cancel(bot, update):
    return ConversationHandler.END


extra_conv = ConversationHandler(
    entry_points=[extra],
    states={
        RunState.EXTRA_START: [extra_start],
        RunState.EXTRA_EXIT: [extra_exit]
    },
    fallbacks=[cancel]
)
