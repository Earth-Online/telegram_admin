#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot command
"""
import logging
import pickle
from datetime import datetime, time, timedelta
from typing import List

from telegram import ForceReply
from telegram import ParseMode
from telegram import Update, Bot, MessageEntity
from telegram import User as TgUser
from telegram.chatmember import ChatMember
from telegram.ext import ConversationHandler, Job, JobQueue
from telegram.ext.dispatcher import run_async
from telegram.ext.filters import Filters
from telegram.chat import Chat

from admin import update_admin_list, update_ban_list
from config import CHAT_DATA_FILE, USER_DATA_FILE, CONV_DATA_FILE
from constant import START_MSG, ADD_ADMIN_OK_MSG, BOT_NO_ADMIN_MSG, BOT_IS_ADMIN_MSG, ID_MSG, ADMIN_FORMAT, \
    GET_ADMINS_MSG, GROUP_FORMAT, BOT_STOP_MSG, INFO_MSG, GLOBAL_BAN_FORMAT, allow_setting, OK, NO, BANWORD_ERROR, \
    BANWORD_FORMAT, GET_BANWORDS_MSG, SET_OK_MSG, BAN_STATE, START_TIME_MSG, STOP_TIME_MSG, UserData, \
    ARG_ERROR_MSG, USERID_ERROR_MSG, RunState, NO_INFO_MSG, NUM_ERROR, ChatData, OpenState, OPITON_ERROR, BOT_RUN_MSG, \
    CLEANWARN_MSG, NO_RUN_MSG, LINK_FORMAT, GLOBAN_BAN_MSG, UNGLOBAN_BAN_MSG, MAXWARN_MSG, TIMEfLOOD_MSG, FLOOD_MSG, \
    SETTING_MSG, BANWORD_MSG, UNBANWORD_MSG, LANG_MSG, KICK_MSG, LOCK_MSG, UNLOCK_MSG, TIMER_MSG, DELETE_TIMER_MSG, \
    LISTTIMER_MSG, UNAUTOLOCK_MSG, LANG_DICT, e_allow_setting, LIMIT_DICT
from module import DBSession
from module.group import Group
from module.user import User
from tool import command_wrap, check_admin, word_re, get_user_data, get_chat_data, get_conv_data, kick_user, \
    messaage_warp, check_run, time_send_msg, save_jobs


@command_wrap()
@run_async
def start(bot, update):
    """
    send start info
    """
    bot.send_message(chat_id=update.message.chat_id, text=START_MSG)
    session = DBSession()
    user = session.query(User).filter_by(id=update.message.from_user['id']).first()
    if user is None:
        session.add(User(id=update.message.from_user['id']))
    session.commit()
    session.close()


@command_wrap(name="بوت")
@run_async
def ping(bot, update):
    """
    send start info
    """
    pingtime = datetime.now().timestamp() - update.message.date.timestamp()
    bot.send_message(chat_id=update.message.chat_id, text=pingtime)


@command_wrap(name="مطور", pass_args=True)
@run_async
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


@command_wrap(pass_chat_data=True, name="تفعيل")
@run_async
@check_admin()
def run(bot, update, chat_data):
    """Run bot filter function
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if chat_data.get(ChatData.RUN):
        bot.send_message(chat_id=update.message.chat_id, text=BOT_RUN_MSG)
        return
    bot_id = bot.id
    group_info = bot.get_chat_member(update.message.chat_id, bot_id)
    if group_info['status'] != ChatMember.ADMINISTRATOR:
        bot.send_message(chat_id=update.message.chat_id, text=BOT_NO_ADMIN_MSG)
        return
    session = DBSession()
    if update.message.chat.type == Chat.SUPERGROUP:
        group_link = bot.export_chat_invite_link(chat_id=update.message.chat_id)
    else:
        group_link = ""
    group = Group(id=update.message.chat_id, title=update.message.chat.title, link=group_link)
    session.merge(group)
    session.commit()
    session.close()
    chat_data[ChatData.RUN] = True
    bot.send_message(chat_id=update.message.chat_id, text=BOT_IS_ADMIN_MSG)


@command_wrap(pass_args=True, name="ازالة_التحذيرات")
@check_admin()
@check_run()
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
            user_list.append(TgUser(id=_, first_name="temp", is_bot=False))
    if update.message.reply_to_message:
        user_list.append(update.message.reply_to_message.from_user['id'])
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == MessageEntity.TEXT_MENTION:
                user_list.append(entity.user['id'])
    if not len(user_list):
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    user_data = get_user_data()
    for user in user_list:
        user_data[user.id][UserData.WARN] = 0
    bot.send_message(chat_id=update.message.chat_id, text=CLEANWARN_MSG)


@command_wrap(name='ايدي')
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


@command_wrap(name="المشرفين")
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


@command_wrap(name="المجموعات")
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
    if groups is None:
        bot.send_message(chat_id=update.message.chat_id, text=NO_INFO_MSG)
        session.close()
        return
    ret_text = ""
    for group in groups:
        ret_text = ret_text + GROUP_FORMAT.format(group_title=group.title, group_id=group.id,
                                                  group_link=group.link)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text, parse_mode=ParseMode.MARKDOWN)
    session.close()


@command_wrap(pass_chat_data=True, name="تعطيل")
@check_admin()
@check_run()
@run_async
def stop(bot, update, chat_data):
    """
    Stop bot filer function
    :param chat_data:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if not chat_data.get(ChatData.RUN):
        bot.send_message(chat_id=update.message.chat_id, text=NO_RUN_MSG)
        return
    chat_data[ChatData.RUN] = False
    bot.send_message(chat_id=update.message.chat_id, text=BOT_STOP_MSG)


@command_wrap(name="الرابط")
@check_admin()
@check_run()
@run_async
def link(bot, update):
    """

    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    # TODO 更新数据库
    if not update.message.chat.type == Chat.SUPERGROUP:
        bot.send_message(chat_id=update.message.chat_id, text="not supergroup")
        return
    group_link = bot.export_chat_invite_link(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, parse_mode=ParseMode.MARKDOWN,
                     text=LINK_FORMAT.format(link=group_link))


@command_wrap(name="معلومات")
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


@command_wrap(pass_args=True, name="حظر_عام")
@check_admin()
@run_async
def globalban(bot, update, args):
    """
    globalban a user
    :param args:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    ban_user_list = []
    for _ in args:
        if _.isdigit():
            ban_user_list.append(TgUser(id=_, first_name="not get", is_bot=False))
    for entity in update.message.parse_entities(MessageEntity.TEXT_MENTION).keys():
        ban_user_list.append(entity.user)
    if not len(ban_user_list):
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    bot.send_message(chat_id=update.message.chat_id, text=GLOBAN_BAN_MSG)
    ban_user(user_list=ban_user_list, ban=True)
    update_ban_list()


@command_wrap(pass_args=True, name="الغاء_العام")
@check_admin()
@run_async
def unglobalban(bot, update, args):
    """
    cancel a user globalbanr
    :param args:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    ban_user_list = []
    for _ in args:
        if _.isdigit():
            ban_user_list.append(TgUser(id=_, first_name="not get", username="not get", is_bot=False))
    for entity in update.message.parse_entities(MessageEntity.TEXT_MENTION).keys():
        ban_user_list.append(entity.user)
    if not len(ban_user_list):
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    ban_user(user_list=ban_user_list, ban=False)
    bot.send_message(chat_id=update.message.chat_id, text=UNGLOBAN_BAN_MSG)
    update_ban_list()


@command_wrap(name="المحظورين_عام")
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
        ret_text = ret_text + GLOBAL_BAN_FORMAT.format(user_id=data.id)
    session.close()
    if ret_text == "":
        bot.send_message(chat_id=update.message.chat_id, text=NO_INFO_MSG)
        return
    bot.send_message(chat_id=update.message.chat_id, text=ret_text, parse_mode=ParseMode.MARKDOWN)


@command_wrap(pass_chat_data=True, pass_args=True, name="التحذيرات")
@check_admin()
@check_run()
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
        bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)
        return
    if not args[0].isdigit():
        bot.send_message(update.message.chat_id, text=NUM_ERROR)
    chat_data[ChatData.MAXWARN] = int(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=MAXWARN_MSG.format(num=args[0]))


@command_wrap(pass_chat_data=True, pass_args=True, name="وقت_التكرار")
@check_admin()
@check_run()
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
        bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)
        return
    if not args[0].isdigit():
        bot.send_message(update.message.chat_id, text=NUM_ERROR)
    chat_data[ChatData.FLOOD_TIME] = int(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=TIMEfLOOD_MSG.format(num=args[0]))


@command_wrap(pass_chat_data=True, pass_args=True, name="تعيين_التكرار")
@check_admin()
@check_run()
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
        bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)
        return
    if not args[0].isdigit():
        bot.send_message(update.message.chat_id, text=NUM_ERROR)
    chat_data[ChatData.FLOOD_NUM] = int(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=FLOOD_MSG.format(num=args[0]))


@command_wrap(pass_chat_data=True, pass_args=True, name="تعيين_الرسائل")
@check_admin()
@check_run()
@run_async
def setmaxmessage(bot, update, args, chat_data):
    """
    :param args:
    :param chat_data:
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    if len(args) == 0 and chat_data.get(ChatData.MAXFLOOD):
        chat_data.pop(ChatData.MAXFLOOD)
        bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)
        return
    if not args[0].isdigit():
        bot.send_message(update.message.chat_id, text=NUM_ERROR)
    chat_data[ChatData.MAXFLOOD] = int(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)


@command_wrap(pass_chat_data=True, name="الاعدادات")
@check_admin()
@check_run()
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
        state = OK
        if all([limit.get(i) for i in LIMIT_DICT.get(setting)]):
            state = NO
        ret_text = ret_text + SETTING_MSG.format(setting=setting,state=state)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)


@command_wrap(pass_chat_data=True, pass_args=True, name="منع")
@check_admin()
@check_run()
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
    bot.send_message(chat_id=update.message.chat_id, text=BANWORD_MSG.format(word=" ".join(args)))


@command_wrap(pass_chat_data=True, pass_args=True, name="سماح")
@check_admin()
@check_run()
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
    bot.send_message(chat_id=update.message.chat_id, text=UNBANWORD_MSG.format(word=" ".join(args)))
    if not len(group_banwords):
        chat_data[ChatData.BANWORD_RE] = None
        return
    chat_data[ChatData.BANWORD_RE] = word_re(group_banwords)


@command_wrap(pass_chat_data=True, name="منع")
@check_admin()
@check_run()
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


@command_wrap(pass_chat_data=True, pass_args=True, name="اللغة")
@run_async
@check_admin()
@check_run()
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
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    if args[0] not in list(LANG_DICT.keys()):
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    args[0] = LANG_DICT.get(args[0])
    ban_list: list = chat_data.get(ChatData.LANG, [])
    if args[1] == OpenState.CLODE:
        ban_list.append(args[0])
        chat_data[ChatData.LANG] = ban_list
    elif args[1] == OpenState.OPEN:
        if args[0] in ban_list:
            ban_list.remove(args[0])
        chat_data[ChatData.LANG] = ban_list
    else:
        bot.send_message(chat_id=update.message.chat_id, text=OPITON_ERROR)
        return
    bot.send_message(chat_id=update.message.chat_id, text=LANG_MSG.format(lang=args[0], state=args[1]))


@command_wrap(name="حفظ")
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


@command_wrap(pass_args=True, name="طرد")
@check_admin()
@check_run()
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
    bot.send_message(chat_id=update.message.chat_id, text=KICK_MSG.format(ids=" ".join(kick_user_list)))


@command_wrap(pass_args=True, pass_chat_data=True, name="قفل")
@check_admin()
@check_run()
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
    bot.send_message(chat_id=update.message.chat_id, text=LOCK_MSG)


@command_wrap(pass_chat_data=True, name="فتح")
@check_admin()
@check_run()
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
    bot.send_message(chat_id=update.message.chat_id, text=UNLOCK_MSG)


@command_wrap(name="قفل_مؤقت")
@check_admin()
@check_run()
def autolock(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    update.message.reply_text(text=START_TIME_MSG, reply_markup=ForceReply())
    return RunState.START_TIME


@command_wrap(pass_job_queue=True, pass_args=True, name="توقيت")
@check_admin()
@check_run()
@run_async
def timer(bot, update, job_queue, args):
    """

    :param bot:
    :param update:
    :param job_queue:
    :param args:
    :type job_queue:  JobQueue
    :return:
    """
    if len(args) < 2:
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    try:
        day = datetime.strptime(args[0], "%H:%M")
        time = day.time()
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id, text=ARG_ERROR_MSG)
        return
    job_queue.run_repeating(callback=time_send_msg, context=[args[0], args[1], update.message.chat_id],
                            name=update.message.chat_id, interval=timedelta(days=1), first=time)
    bot.send_message(chat_id=update.message.chat_id, text=TIMER_MSG)


@command_wrap(pass_job_queue=True, name="التواقيت")
@check_admin()
@check_run()
@run_async
def listtimer(bot, update, job_queue):
    """

    :param bot:
    :param update:
    :param job_queue:
    :return:
    """
    jobs: List[Job] = job_queue.get_jobs_by_name(update.message.chat_id)
    if not len(jobs):
        bot.send_message(chat_id=update.message.chat_id, text=NO_INFO_MSG)
        return
    ret_text = ""
    for job in jobs:
        if not job.removed:
            ret_text = ret_text + LISTTIMER_MSG.format(time=job.context[0], msg=job.context[1])
    if not ret_text:
        bot.send_message(chat_id=update.message.chat_id, text=NO_INFO_MSG)
        return
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)


@command_wrap(pass_job_queue=True, pass_args=True, name="حذف_توقيت")
@check_admin()
@check_run()
@run_async
def deletetimer(bot, update, job_queue, args):
    if not len(args) or not args[0].isdigit():
        bot.send_message(chat_id=update.message.chat_id, text=NUM_ERROR)
        return
    jobs = job_queue.get_jobs_by_name(update.message.chat_id)
    if len(jobs) < int(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text=NUM_ERROR)
        return
    jobs[int(args[0])].schedule_removal()
    bot.send_message(chat_id=update.message.chat_id, text=DELETE_TIMER_MSG)


@command_wrap(pass_chat_data=True, name="الغاء_القفل")
@check_admin()
@check_run()
@run_async
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
    bot.send_message(chat_id=update.message.chat_id, text=UNAUTOLOCK_MSG)


@command_wrap(name="الغاء")
@check_admin()
def cancel(bot, update):
    """
    :param bot:
    :type bot: Bot
    :param update:
    :type update: Update
    :return:
    """
    return ConversationHandler.END


@messaage_warp(filters=Filters.all, pass_chat_data=True)
@check_admin()
@check_run()
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
        return RunState.START_TIME
    try:
        time = datetime.strptime(update.message.text, "%H:%M")
    except ValueError:
        update.message.reply_text(text=START_TIME_MSG, reply_markup=ForceReply())
        return RunState.START_TIME
    chat_data[ChatData.AUTO_LOOK_START] = time
    update.message.reply_text(text=STOP_TIME_MSG, reply_markup=ForceReply())
    return RunState.STOP_TIME


@messaage_warp(filters=Filters.all, pass_chat_data=True)
@check_admin()
@check_run()
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
        return RunState.STOP_TIME
    try:
        locktime = datetime.strptime(update.message.text, "%H:%M")
    except ValueError:
        update.message.reply_text(text=START_TIME_MSG, reply_markup=ForceReply())
        return RunState.STOP_TIME
    chat_data[ChatData.AUTO_LOOK_STOP] = locktime
    bot.send_message(chat_id=update.message.chat_id, text=SET_OK_MSG)
    return ConversationHandler.END


def save_data(bot=None, job=None):
    user_data = get_user_data()
    chat_data = get_chat_data()
    with open(CHAT_DATA_FILE, 'wb+') as f:
        pickle.dump(chat_data, f)
    with open(USER_DATA_FILE, 'wb+') as f:
        pickle.dump(user_data, f)
    if job:
        if isinstance(job, JobQueue):
            save_jobs(job)
        else:
            save_jobs(job.job_queue)
    logging.info("save data ok")


def ban_user(user_list, ban=True):
    session = DBSession()
    for user_data in user_list:
        session.merge(User(id=user_data.id, isban=ban, username=user_data.username))
    session.commit()
    session.close()
