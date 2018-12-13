#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
send msg constar
"""
import re

# /start msg
START_MSG = "أهلا بك في بوت الحماية"

# /add msg
ADD_ADMIN_OK_MSG = "تم اضافة العضو مطور"

# some arg error msg. example not get arg
ARG_ERROR_MSG = "خطأ"

# error user id msg . example /add meisnotid
USERID_ERROR_MSG = "ايدي العضو غير صحيح"

# option error example /lang zh-cn  Iwillopen
OPITON_ERROR = "اللغة غير مدعومة"

# error num example /maxwarns error
NUM_ERROR = "قم  ىتعيين رقم صحيح"

# not get some info. example not group. but use /groups
NO_INFO_MSG = "لا يوجد معلومات"

# When not supergroup ,example use /link. ! export link only supergroup
NO_SUPERGROUP_MSG = "المجموعات الخارقة فقط"

# /run msg
BOT_NO_ADMIN_MSG = "يجب ان اكون مشرف في المجموعة"

BOT_IS_ADMIN_MSG = "✅ تم تفعيل المجموعة"

BOT_RUN_MSG = "المجموعة مفعلة مسبقا"

# When the bot is not running, run some commands
NO_RUN_MSG = "المجموعة غير مفعلة"

# /clearnwarns msg
CLEANWARN_MSG = "تم ازالة جميع تحذيرات العضو"

# /id msg  {user_id} is user id {group_id} is group id. not change it. {xxx} Also please don't change it
ID_MSG = """
🔸 ايدي العضو : {user_id}
🔹 ايدي المجموعة : {group_id}
"""

# /admins msg
GET_ADMINS_MSG = """
👮‍♂ منشئ المجموعة :
{creators}
💂‍♂ المشرفين :
{admins}
"""
ADMIN_FORMAT = """- [{username}](tg://user?id={user_id})\n"""

# /groups msg  line format
GROUP_FORMAT = "{group_title} |{group_id}| [GroupLink]({group_link})\n"

# /link msg support markdown
LINK_FORMAT = "{link}"

# /info msg
INFO_MSG = """
🔸 اسم العضو : {username}
🔸 ايدي العضو : {user_id}
"""

# /globalban msg
GLOBAN_BAN_MSG = "تم حظر العضو من جميع المجموعات"

# /unglobalban msg
UNGLOBAN_BAN_MSG = "تم ازالة الحظر العام عن العضو"

# /globalban_list msg line format support markdown.
GLOBAL_BAN_FORMAT = """[{user_id}](tg://user?id={user_id})\n"""

# /maxwarns msg
MAXWARN_MSG = "تم تعيين الحد الاقصى للتحذيرات : {num}"

# /settimeflood msg
TIMEfLOOD_MSG = "تم تعيين وقت التكرار : {num}"

# /setflood msg
FLOOD_MSG = "تم تعيين الحد الاقصى للتكرار : {num}"

# /setting msg line format
SETTING_MSG = "{setting}{state}\n"

# state flag
OK = "✅"
NO = "❌"

# /banword msg {word} == args exapmle /banword a b c {word} = a b c
BANWORD_MSG = "تم حظر الكلمة : {word}"

# /unbanword msg
UNBANWORD_MSG = "تم ازالة حظر الكلمة : {word}"

# /banwords msg {word} = a word
GET_BANWORDS_MSG = """
⛔️ الكلمات المحظورة : 
{banwords}
"""
BANWORD_FORMAT = """• {word}\n"""

# /stop msg
BOT_STOP_MSG = "تم ازالة البوت"

# /lang msg
LANG_MSG = "تم {lang} {state}"

# /kick msg
KICK_MSG = "تم طرد العضو {ids}"

# /lock msg
LOCK_MSG = "تم قفل .."

# /unlock msg
UNLOCK_MSG = "تم السماح .."

# /autolock msg
START_TIME_MSG = "ارسل وقت قفل المجموعة مثل : 01:00"
STOP_TIME_MSG = "ارسل وقت فتح المجموعة : 02:00"

# /unautolock msg
UNAUTOLOCK_MSG = "تم الغاء قفل المجموعة"
# /timer  msg
TIMER_MSG = "تم تعيين توقيت الرسالة"

# /listtimer line format
LISTTIMER_MSG = "{time} {msg}\n"

# /deletetimer msg
DELETE_TIMER_MSG = "تم ازالة الرسالة المؤقتة"

# warn user msg
WARN_MSG = "تحذير، لا يمكنك ارسال هذا النوع من الوسائط"

# /bcuser /bcgroups format not supoort
NO_SUPPORT_FORMAT = "هذه الصغية غير مدعومة"

# /bcuser ....   msg
USER_FORWARD_START = "ارسل الرسالة الان"
USER_FORWARD_STOP = "تم ارسالة الرسالة للجميع"

# /vipuser msg
VIPUSER_MSG = "add {ids} ok"

# /extra msg
EXTRA_MSG = "Send Message Now :"
EXTRA_EXIT_MSG = "Send Reply now:"
EXTRA_SAVE_MSG = "Done Save"

# /topuser msg
TOPUSER_FORMAT = "{sentence} : {frequency}"

ADMIN = "المشرف"

SET_OK_MSG = "تم التعيين"

NO_GET_USENAME_MSG = """لم استطع الحصول على معرف العضو. """

RUN = 1
STOP = 0

MAXWARNS_ERROR = "خطأ، قم بالمحاولة مرة اخرى"
BANWORD_ERROR = "خطأ، قم بالمحاولة مرة اخرى"


class OpenState:
    OPEN = "فتح"
    CLODE = "قفل"


class RunState:
    RUN = 1
    STOP = 0
    START_TIME = 999
    STOP_TIME = 1000
    USER_FORWARD = 888
    GRUOP_FORWARD = 889
    forwardgroups = 777
    forwardusers = 666
    EXTRA_START = 433
    EXTRA_EXIT = 434

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
    "الماركداون": [BanMessageType.BOLD, BanMessageType.ITALIC, BanMessageType.CODE, BanMessageType.URL],
    'الويب': [BanMessageType.URL, BanMessageType.TEXT_LINK],
    'الفيديو': [BanMessageType.VIDEO],
    'الصور': [BanMessageType.PHOTO],
    'الموسيقى': [BanMessageType.AUDIO],
    'الملفات': [BanMessageType.DOCS],
    'النصوص': [BanMessageType.TEXT],
    'التوجيه': [BanMessageType.FORWARD],
    'الالعاب': [BanMessageType.GAME],
    'الملصقات': [BanMessageType.STICKER],
    'المتحركة': [BanMessageType.GIF],
    'الايموجي': [BanMessageType.EMOJI],
    'الهاشتاق': [BanMessageType.HASHTAG],
    'المنشن': [BanMessageType.MENTION],
    'التسجيلات': [BanMessageType.VIDEONOTE],
    'الروابط': [BanMessageType.URL],
    'الاشعارات': [BanMessageType.ADDGROUP],
    'الكلمات': [BanMessageType.BANWORD],
    'التحذير': [BanMessageType.WARN],
    'الكود': [BanMessageType.CODE],
    'العريض': [BanMessageType.BOLD],
    'المائل': [BanMessageType.ITALIC],
    'المخفي': [BanMessageType.TEXT_LINK],
    'الارقام': [BanMessageType.NUMBERS],
    'التكرار': [BanMessageType.FLOOD],
    'اللغة': [BanMessageType.LANG],
    'الاعلانات': [BanMessageType.TG_LINK],
    'المواقع': [BanMessageType.LOCATION],
    'الارسال': [BanMessageType.MAXMSG],
    'المكان': [BanMessageType.VENUE],
    'الفواتير': [BanMessageType.INVOICE],
}

LANG_DICT = {
    # add it. if you not add one limit line. will Unable to set a limit
    "الانجليزية": "en",
    "الفارسية": "fa",
    "العربية": "ar",
}


class UserData:
    WARN = "warn"
    MSG_DATA = "msg_data"
    MAXMSG_DATA = "maxmsg"
    TMP = "tmp"


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
    VIPUSER = "vipuser"
    EXTRA = "extra"


TELEGRAM_DOMAIN = ["t.me", "telegram.me"]
MARKDOWN_BAN = [BanMessageType.BOLD, BanMessageType.ITALIC, BanMessageType.CODE, BanMessageType.URL]
e_allow_setting = [BanMessageType.__dict__[key] for key in filter(lambda x: x[0] != "_", BanMessageType.__dict__)]
# allow_setting = allow_setting + list(LIMIT_DICT.keys())
allow_setting = list(LIMIT_DICT.keys())

allow_str = "|".join(allow_setting)
SETTING_RE = re.compile(f"^[!|#|/]*({allow_str})\\s+({OpenState.OPEN}|{OpenState.CLODE})$")
NUM_RE = re.compile(r"\d")

BANWORD_KEY = "banwordre"
LANGDATA_KEY = "lang_data"
TIME_END = "timeend"
BAN_STATE = "ban_state"
AUTO_LOOK_START = "look_start"
AUTO_LOOK_STOP = "look_stop"
