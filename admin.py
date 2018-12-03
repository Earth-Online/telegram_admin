#!coding:utf-8
#  Created by bluebird on 2018/12/3
"""
admin check and cache
"""
from config import ADMIN
from module import DBSession
from module.user import User

admin_list = []


def update_admin_list():
    session = DBSession()
    db_admin = session.query(User.id).all()
    global admin_list
    admin_list = ADMIN + db_admin


def user_is_admin(user_id):
    return user_id in admin_list
