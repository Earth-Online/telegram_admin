#!coding:utf-8
#  Created by bluebird on 2018/12/7
"""
docs
"""
from time import sleep

from telegram.ext import ConversationHandler

from config import SEND_SLEEP
from module import DBSession, Group
from module.user import User
from tool import command_wrap, check_admin, messaage_warp
from constant import RunState, USER_FORWARD_START, USER_FORWARD_STOP, NO_SUPPORT_FORMAT
from telegram.ext.filters import Filters
from telegram import Update, Bot, ParseMode


@command_wrap()
@check_admin()
def bcgroups(bot, update):
    update.message.reply_text(text=USER_FORWARD_START)
    return RunState.GRUOP_FORWARD


@command_wrap()
@check_admin()
def bcusers(bot, update):
    update.message.reply_text(text=USER_FORWARD_START)
    return RunState.USER_FORWARD


@command_wrap()
@check_admin()
def forwardusers(bot, update):
    update.message.reply_text(text=USER_FORWARD_START)
    return RunState.forwardgroups


@command_wrap()
@check_admin()
def forwardgroups(bot, update):
    update.message.reply_text(text=USER_FORWARD_START)
    return RunState.forwardusers


@command_wrap()
@check_admin()
def cancel(bot, update):
    return ConversationHandler.END


@messaage_warp(filters=Filters.all)
def send_group(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return
    """
    session = DBSession()
    groups = session.query(Group).all()
    send_admin_msg(users=groups, bot=bot, update=update)
    bot.send_message(chat_id=update.message['id'], text=USER_FORWARD_STOP)
    session.close()
    return ConversationHandler.END


@messaage_warp(filters=Filters.all)
def send_user(bot, update):
    session = DBSession()
    users = session.query(User).all()
    if not (Filters.text(update.message) | Filters.sticker(update.message) | Filters.photo(
            update.message) | Filters.video(update.message)
            | Filters.document(update.message)):
        bot.send_message(chat_id=update.message.id, text=NO_SUPPORT_FORMAT)
        return
    send_admin_msg(users=users, bot=bot, update=update)
    bot.send_message(chat_id=update.message.id, text=USER_FORWARD_STOP)
    session.close()
    return ConversationHandler.END


@messaage_warp(filters=Filters.all)
def forward_user(bot, update):
    session = DBSession()
    users = session.query(User).all()
    for user in users:
        update.message.forward(user.id)
        sleep(SEND_SLEEP)
    session.close()
    return ConversationHandler.END


@messaage_warp(filters=Filters.all)
def forward_group(bot, update):
    session = DBSession()
    users = session.query(Group).all()
    for user in users:
        update.message.forward(user.id)
        sleep(SEND_SLEEP)
    session.close()
    return ConversationHandler.END


def send_admin_msg(users, bot, update):
    if Filters.text(update.message):
        for user in users:
            bot.send_message(chat_id=user.id, text=update.message.text, parse_mode=ParseMode.HTML)
            sleep(1)
    elif Filters.sticker(update.message):
        for user in users:
            bot.send_sticker(chat_id=user.id, sticker=update.message.sticker.file_id)
            sleep(1)
    elif Filters.photo(update.message):
        for photo in update.message.photo:
            for user in users:
                bot.send_photo(chat_id=user.id, photo=photo.file_id, caption=update.message.caption)
                sleep(1)
    elif Filters.video(update.message):
        for user in users:
            bot.send_video(chat_id=user.id, video=update.message.video.file_id, caption=update.message.caption)
            sleep(1)
    elif Filters.document(update.message):
        for user in users:
            bot.send_document(chat_id=user.id, document=update.message.document.file_id,
                              caption=update.message.caption)
            sleep(1)
    else:
        return


conv_handle = ConversationHandler(
    entry_points=[bcgroups, bcusers, forwardusers, forwardgroups],
    states={
        RunState.forwardgroups: [forward_group],
        RunState.forwardusers: [forward_user],
        RunState.USER_FORWARD: [send_user],
        RunState.GRUOP_FORWARD: [send_group]
    },
    fallbacks=[cancel]
)
