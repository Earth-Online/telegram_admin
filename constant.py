#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
send msg constar
"""
import re

# /start msg
START_MSG = "bot run ok"

# /add msg
ADD_ADMIN_OK_MSG = "add ok"

# some arg error msg. example not get arg
ARG_ERROR_MSG = "arg error"

# error user id msg . example /add meisnotid
USERID_ERROR_MSG = "error user id"

# option error example /lang zh-cn  Iwillopen
OPITON_ERROR = "error option"

# error num example /maxwarns error
NUM_ERROR = "not a effective number"

# not get some info. example not group. but use /groups
NO_INFO_MSG = "not have some info"

# When not supergroup ,example use /link. ! export link only supergroup
NO_SUPERGROUP_MSG = "group not is supergroup"

# /run msg
BOT_NO_ADMIN_MSG = "I SHOULD BE ADMIN IN THE GROUP"

BOT_IS_ADMIN_MSG = "✅ Done Active The Group"

BOT_RUN_MSG = "The group alredy Actived"

# When the bot is not running, run some commands
NO_RUN_MSG = "bot not run. pleser use /run"

# /clearnwarns msg
CLEANWARN_MSG = "clearn warn ok"

# /id msg  {user_id} is user id {group_id} is group id. not change it. {xxx} Also please don't change it
ID_MSG = """
🔸 your id : {user_id}LINKTEXT 
🔹 group id : {group_id}
"""

# /admins msg
GET_ADMINS_MSG = """
👮‍♂ Groups Creator :
{creators}
💂‍♂ Group Admins :
{admins}
"""
ADMIN_FORMAT = """- [{username}](tg://user?id={user_id})\n"""

# /groups msg  line format
GROUP_FORMAT = "{group_title} |{group_id}| [GroupLink]({group_link})\n"

# /link msg support markdown
LINK_FORMAT = "{link}"

# /info msg
INFO_MSG = """
🔸 USER NAME : {username}
🔸 USER ID : {user_id}
"""

# /globalban msg
GLOBAN_BAN_MSG = "ban user ok"

# /unglobalban msg
UNGLOBAN_BAN_MSG = "unban user ok"

# /globalban_list msg line format support markdown.
GLOBAL_BAN_FORMAT = """[{user_id}](tg://user?id={user_id})\n"""

# /maxwarns msg
MAXWARN_MSG = "Done set max warns {num}"

# /settimeflood msg
TIMEfLOOD_MSG = "Done set time flood {num}"

# /setflood msg
FLOOD_MSG = "Done set flood {num}"

# /setting msg line format
SETTING_MSG = "{setting}{state}\n"

# state flag
OK = "✅"
NO = "❌"

# /banword msg {word} == args exapmle /banword a b c {word} = a b c
BANWORD_MSG = "done banword {word}"

# /unbanword msg
UNBANWORD_MSG = "done unbanword {word}"

# /banwords msg {word} = a word
GET_BANWORDS_MSG = """
⛔️ ban words : 
{banwords}
"""
BANWORD_FORMAT = """• {word}\n"""

# /stop msg
BOT_STOP_MSG = "bot stop"

# /lang msg
LANG_MSG = "Done {lang} {state}"

# /kick msg
KICK_MSG = "kick {ids}"

# /lock msg
LOCK_MSG = "lock start"

# /unlock msg
UNLOCK_MSG = "lock stop"

# /autolock msg
START_TIME_MSG = "send lock group time format example 01:00"
STOP_TIME_MSG = "send open group time  format example 02:00"

# /unautolock msg
UNAUTOLOCK_MSG = "autolock stop"
# /timer  msg
TIMER_MSG = "ok"

# /listtimer line format
LISTTIMER_MSG = "{time} {msg}\n"

# /deletetimer msg
DELETE_TIMER_MSG = "OK"

# warn user msg
WARN_MSG = "not send"

# /bcuser /bcgroups format not supoort
NO_SUPPORT_FORMAT = "not support format"

# /bcuser ....   msg
USER_FORWARD_START = "Send The Message Now"
USER_FORWARD_STOP = "Done Send message to all"

ADMIN = "administrator"

SET_OK_MSG = "setting ok"

NO_GET_USENAME_MSG = """Warning: Due to api restrictions, usernames cannot be obtained from user_id.The user name of 
this user will not be included in the added data. """

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
    FORWARD = 'forward_date'
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
    MAXMSG = "maxmsg"
    #   LINKTEXT = "linktext"
    #   MARKDOWN = "markdown"
    EMOJI = "emoji"
    HASHTAG = "hashtag"
    MENTION = "mention"
    WARN = "warn"
    BANWORD = "banword"
    URL = "url"
    VIDEONOTE = "videonote"
    LINK = "link"
    ADDGROUP = "addgroup"


LIMIT_DICT = {
    # add it.  format word:[open limit] example "urllimit":[BanMessageType.URL],
    # if you not add one limit line. will Unable to set a limit
    "markdown": [BanMessageType.BOLD, BanMessageType.ITALIC, BanMessageType.CODE, BanMessageType.URL],
    BanMessageType.LINK: [BanMessageType.URL, BanMessageType.TEXT_LINK],
}

LANG_DICT = {
    # add it. if you not add one limit line. will Unable to set a limit
    "english": "en",
}


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


TELEGRAM_DOMAIN = ["t.me", "telegram.me"]
MARKDOWN_BAN = [BanMessageType.BOLD, BanMessageType.ITALIC, BanMessageType.CODE, BanMessageType.URL]
# allow_setting = [BanMessageType.__dict__[key] for key in filter(lambda x: x[0] != "_", BanMessageType.__dict__)]
# allow_setting = allow_setting + list(LIMIT_DICT.keys())
allow_setting = list(LIMIT_DICT.keys())

allow_str = "|".join(allow_setting)
SETTING_RE = re.compile(f"^[!|#|/]*({allow_str})\\s+(on|off)$")
NUM_RE = re.compile(r"\d")

BANWORD_KEY = "banwordre"
LANGDATA_KEY = "lang_data"
TIME_END = "timeend"
BAN_STATE = "ban_state"
AUTO_LOOK_START = "look_start"
AUTO_LOOK_STOP = "look_stop"
