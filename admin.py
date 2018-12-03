#!coding:utf-8
#  Created by bluebird on 2018/12/3
"""
admin check and cache
"""
import logging
from config import ADMIN
from module import DBSession
from module.user import User

admin_list = []


def update_admin_list():
    session = DBSession()
    db_admin = session.query(User.id).all()
    global admin_list
    admin_list = ADMIN + db_admin
    logging.debug(f"admin list {admin_list}")
    session.close()


def user_is_admin(user_id):
    logging.debug(f'{user_id} is admin {user_id in admin_list}')
    return user_id in admin_list