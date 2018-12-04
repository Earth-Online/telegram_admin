#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
send msg constar
"""

START_MSG = "bot run ok"

ADD_ADMIN_OK_MSG = "add ok"

BOT_NO_ADMIN_MSG = "I SHOULD BE ADMIN IN THE GROUP"

BOT_IS_ADMIN_MSG = "✅ Done Active The Group"

BOT_STOP_MSG = "bot stop"

INFO_MSG = """
🔸 USER NAME : {username}
🔸 USER ID : {user_id}
"""

WARN_MSG = "not send"

ADMIN = "administrator"
ID_MSG = """
🔸 your id : {user_id}
🔹 group id : {group_id}
"""

GET_ADMINS_MSG = """
👮‍♂ Groups Creator :
{creators}
💂‍♂ Group Admins :
{admins}
"""

NO_GET_USENAME_MSG = """Warning: Due to api restrictions, usernames cannot be obtained from user_id.The user name of 
this user will not be included in the added data. """

GLOBAL_BAN_FORMAT = """[{user_name}](tg://user?id={user_id})"""
ADMIN_FORMAT = """- [{username}](tg://user?id={user_id})"""
GROUP_FORMAT = "{group_title} |{group_id}| [GroupLink]({group_link})"

RUN = 1
STOP = 0


class BanMessageType:
    VIDEO = 'video'
    PHOTO = 'photo'
    AUDIO = 'audio'
    DOCS = 'document'
    TEXT = 'text'
    ALL = 'all'
    FORWARD = 'forward'
    GAME = 'game'
    STICKER = 'sticker'
    VOICE = 'voice'
    CONTACT = 'contact'
    LOCATION = 'location'
    VENUE = 'venue'
    INVOICE = 'Invoice'
    TG_LINK = 'telegramlinks'
    LANG = 'language'


TELEGRAM_DOMAIN = ["t.me", "telegram.me"]
