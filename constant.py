#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
send msg constar
"""
import re

# send msf
START_MSG = "bot run ok"

ADD_ADMIN_OK_MSG = "add ok"

SET_OK_MSG = "setting ok"

ARG_ERROR_MSG = "arg error"

USERID_ERROR_MSG = "error user id"

BOT_NO_ADMIN_MSG = "I SHOULD BE ADMIN IN THE GROUP"

BOT_IS_ADMIN_MSG = "✅ Done Active The Group"

NO_RUN_MSG = "bot not run. pleser use /run"

NO_SUPPORT_FORMAT = "not support format"

BOT_STOP_MSG = "bot stop"

NO_INFO_MSG = "not have some info"

NUM_ERROR = "not a effective number"

USER_FORWARD_START = "Send The Message Now"
USER_FORWARD_STOP = "Done Send message to all"

OPITON_ERROR = "error option"

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

START_TIME_MSG = "send lock group time format example 01:00"
STOP_TIME_MSG = "send open group time  format example 02:00"

GLOBAL_BAN_FORMAT = """[{user_id}](tg://user?id={user_id})\n"""
ADMIN_FORMAT = """- [{username}](tg://user?id={user_id})\n"""
GROUP_FORMAT = "{group_title} |{group_id}| [GroupLink]({group_link})\n"

RUN = 1
STOP = 0
OK = "✅"
NO = "❌"

MAXWARNS_ERROR = "command error.command usage: /maxwarns <num>"
BANWORD_ERROR = "command error.command usage: /banword <banword>"


class OpenState:
    OPEN = "on"
    CLODE = "off"


class RunState:
    RUN = 1
    STOP = 0
    START_TIME = 999
    STOP_TIME = 1000
    USER_FORWARD = 888
    GRUOP_FORWARD = 889
    forwardgroups = 777
    forwardusers = 666


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
    CONTACT = 'contact'
    LOCATION = 'location'
    VENUE = 'venue'
    INVOICE = 'Invoice'
    TG_LINK = 'telegramlinks'
    LANG = 'lang'
    FLOOD = "flood"
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
    WARN = "warn"
    BANWORD = "banword"
    URL = "url"
    VIDEONOTE = "videonote"
    LINK = "link"


class UserData:
    WARN = "warn"
    MSG_DATA = "msg_data"
    MAXMSG_DATA = "maxmsg"


class ChatData:
    MAXWARN = "maxwarn"
    MAXFLOOD = "maxflood"
    FLOOD_TIME = "time"
    FLOOD_NUM = "flood_num"
    BANWORD = "banword"
    BANWORD_RE = "banword_re"
    LANG = "lang"
    LOCKTIME = "locktime"
    BANSTATE = "ban_state"
    AUTO_LOOK_START = "look_start"
    AUTO_LOOK_STOP = "look_stop"
    RUN = "run"


LIMIT_DICT = {
    BanMessageType.MARKDOWN: [BanMessageType.BOLD, BanMessageType.ITALIC, BanMessageType.CODE, BanMessageType.URL],
    BanMessageType.FORWARD: ["forward_date"],
    BanMessageType.LINK: [BanMessageType.URL, BanMessageType.TEXT_LINK]
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

BANWORD_KEY = "banwordre"
LANGDATA_KEY = "lang_data"
TIME_END = "timeend"
BAN_STATE = "ban_state"
AUTO_LOOK_START = "look_start"
AUTO_LOOK_STOP = "look_stop"
