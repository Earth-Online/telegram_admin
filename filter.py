#!coding:utf-8
#  Created by bluebird on 2018/12/4
"""
docs
"""
from telegram.ext.filters import BaseFilter
from telegram.messageentity import MessageEntity
from urllib.parse import urlparse
from tool import check_ban_state, get_chat_data, get_user_data
from langdetect import detect, DetectorFactory
from datetime import datetime
from emoji import emoji_count
from constant import TELEGRAM_DOMAIN, BanMessageType, NUM_RE, BANWORD_KEY, LANGDATA_KEY, TIME_END, AUTO_LOOK_START, \
    AUTO_LOOK_STOP, ChatData
from admin import user_is_admin, user_is_ban


class TelegramLink(BaseFilter):
    def filter(self, message):
        if not check_ban_state(message.chat_id, BanMessageType.TG_LINK):
            return False
        urls = message.parse_entities(types=MessageEntity.URL)
        if len(urls):
            for url in urls.values():
                if urlparse(url).netloc in TELEGRAM_DOMAIN:
                    return True
        urls = message.parse_entities(types=MessageEntity.TEXT_LINK)
        if len(urls):
            for url in urls.keys():
                if urlparse(url.url).netloc in TELEGRAM_DOMAIN:
                    return True
        return False


class Lang(BaseFilter):
    def filter(self, message):
        if not check_ban_state(message.chat_id, BanMessageType.LANG):
            return False
        chat_data: dict = get_chat_data(chat_id=message.chat_id)
        ban_list = chat_data.get(ChatData.LANG, [])
        if not len(ban_list):
            return False
        try:
            ret = detect(message.text) in ban_list
        except DetectorFactory:
            return False
        return ret


class Flood(BaseFilter):

    def filter(self, message):
        if not check_ban_state(message.chat_id, BanMessageType.FLOOD):
            return False
        chat_data: dict = get_chat_data(chat_id=message.chat_id)
        time = chat_data.get(ChatData.FLOOD_TIME)
        num = chat_data.get(ChatData.FLOOD_NUM)
        if not time or not num:
            return
        now_time = datetime.now().timestamp()

        user_data = get_user_data(message.from_user.id)
        msg_data = user_data.get("msg_data", [])
        if len(msg_data) < num:
            msg_data.append(now_time)
            user_data["msg_data"] = msg_data
            return False
        liimt_time = now_time - time
        if msg_data[-1] < liimt_time:
            msg_data = [now_time]
            user_data["msg_data"] = msg_data
            return False
        msg_data = filter(lambda x: x > liimt_time, msg_data)
        if len(list(msg_data)) < num:
            user_data["msg_data"] = msg_data
            return False
        return True


class Gif(BaseFilter):
    def filter(self, message):
        if not check_ban_state(message.chat_id, BanMessageType.GIF):
            return False
        if not message.document:
            return False
        if message['document']['file_name'][-7:] == "gif.mp4":
            return True
        return False


class Emoji(BaseFilter):
    def filter(self, message):
        if not check_ban_state(message.chat_id, BanMessageType.EMOJI):
            return False
        if not message.text:
            return False
        if emoji_count(message.text):
            return True
        return False


class Numbers(BaseFilter):
    def filter(self, message):
        if not check_ban_state(message.chat_id, BanMessageType.NUMBERS):
            return False
        if not message.text:
            return False
        return NUM_RE.search(message.text)


class BanWord(BaseFilter):
    def filter(self, message):
        if not message.text:
            return False
        if not check_ban_state(message.chat_id, BanMessageType.BANWORD):
            return False
        chat_data: dict = get_chat_data(chat_id=message.chat_id)
        re = chat_data.get(ChatData.BANWORD_RE)
        if not re:
            return False
        return re.search(message.text)


class Admin(BaseFilter):
    def filter(self, message):
        return user_is_admin(message.from_user['id'])


class NewMember(BaseFilter):
    def filter(self, message):
        if not message.new_chat_members:
            return False
        return True


class Lock(BaseFilter):
    def filter(self, message):
        time = get_chat_data(message.chat_id).get(ChatData.LOCKTIME)
        if not time:
            return False
        if message.date.timestamp() < time:
            return True
        return False


class AutoLock(BaseFilter):
    def filter(self, message):
        chat_data = get_chat_data(message.chat_id)
        time_start: datetime = chat_data.get(ChatData.AUTO_LOOK_START)
        time_stop: datetime = chat_data.get(ChatData.AUTO_LOOK_STOP)
        if not time_start or not time_stop:
            return False
        if message.date.hour < time_start.hour or message.date.hour > time_stop.hour:
            return False
        if time_start.hour < message.date.hour < time_stop.hour:
            return True
        if message.date.hour == time_start.hour and message.date.minute > time_start.minute:
            return True
        if message.date.hour == time_stop.hour and message.date.minute < time_stop.minute:
            return True
        return False
