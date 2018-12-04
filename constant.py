#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
send msg constar
"""
import re

START_MSG = "bot run ok"

ADD_ADMIN_OK_MSG = "add ok"

SET_OK_MSG = "setting ok"

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

GET_BANWORDS_MSG = """
⛔️ ban words : 
{banwords}
"""

BANWORD_FORMAT = """• {word}\n"""

NO_GET_USENAME_MSG = """Warning: Due to api restrictions, usernames cannot be obtained from user_id.The user name of 
this user will not be included in the added data. """

GLOBAL_BAN_FORMAT = """[{user_name}](tg://user?id={user_id})\n"""
ADMIN_FORMAT = """- [{username}](tg://user?id={user_id})\n"""
GROUP_FORMAT = "{group_title} |{group_id}| [GroupLink]({group_link})\n"

RUN = 1
STOP = 0
OK = "✅"
NO = "❌"

MAXWARNS_ERROR = "command error.command usage: /maxwarns <num>"
BANWORD_ERROR = "command error.command usage: /banword <banword>"


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
    FLOOD = "antiflood"
    NUMBERS = "numbers"
    GIF = "gif"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    TEXT_LINK = 'text_link'
    LINKTEXT = "linktext"
    MARKDOWN = "markdown"
    EMOJI = "emoji"
    HASHTAG = "hashtag"
    MENTION = "mention"
    INLINE = "inline"
    WARN = "warn"
    BANWORD = "banword"
    URL = "url"
    WORD = "banword"
    VIDEONOTE = "videonote"



LIMIT_DICT = {
    BanMessageType.MARKDOWN: [BanMessageType.BOLD, BanMessageType.ITALIC, BanMessageType.CODE, BanMessageType.URL],
    BanMessageType.FORWARD: ["forward_date"]
}


class GetLimit(dict):
    limit_dict = {
        BanMessageType.MARKDOWN: [BanMessageType.BOLD, BanMessageType.ITALIC, BanMessageType.CODE, BanMessageType.URL]
    }

    def __getitem__(self, item):
        return self.limit_dict.get(item)

    def __missing__(self, key):
        return getattr(BanMessageType, key)


TELEGRAM_DOMAIN = ["t.me", "telegram.me"]
MARKDOWN_BAN = [BanMessageType.BOLD, BanMessageType.ITALIC, BanMessageType.CODE, BanMessageType.URL]
allow_setting = [BanMessageType.__dict__[key] for key in filter(lambda x: x[0] != "_", BanMessageType.__dict__)]

allow_str = "|".join(allow_setting)
SETTING_RE = re.compile(f"^({allow_str})\s+(on|off)$")
NUM_RE = re.compile(r"\d")
