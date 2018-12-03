#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
send msg constar
"""

START_MSG = "bot run ok"

ADD_ADMIN_OK_MSG = "add ok"

BOT_NO_ADMIN_MSG = "I SHOULD BE ADMIN IN THE GROUP"

BOT_IS_ADMIN_MSG = "✅ Done Active The Group"

WARN_MSG = "not send"

ADMIN = "administrator"

ID_MSG = """
🔸 your id : {user_id}
🔹 group id : {group_id}
"""

RUN = 1
STOP = 0


class MessageType:
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
