#!coding:utf-8
#  Created by bluebird on 2018/12/3
"""
admin check and cache
"""
import logging

from telegram import Bot
from config import ADMIN
from module import DBSession
from module.user import User
from mwt import MWT
from config import TOKEN

admin_list = []


def update_admin_list():
    logging.debug('update admin list ing')
    session = DBSession()
    db_admin = session.query(User.id).filter_by(isadmin=True).all()
    global admin_list
    admin_list = ADMIN + [int(user.id) for user in db_admin]
    logging.debug(f"admin list {admin_list}")
    session.close()


def user_is_admin(user_id):
    logging.debug(f'{user_id} is admin {user_id in admin_list}')
    return user_id in admin_list


ban_list = []


def update_ban_list():
    logging.debug('update ban list ing')
    session = DBSession()
    db_admin = session.query(User).filter_by(isban=True).all()
    global ban_list
    ban_list = [int(user.id) for user in db_admin]
    logging.debug(f"ban list {ban_list}")
    session.close()


def user_is_ban(user_id):
    logging.debug(f'{user_id} is admin {user_id in admin_list}')
    return user_id in ban_list


@MWT(timeout=60 * 60)
def get_groupadmin(chat_id):
    bot = Bot(token=TOKEN)
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
