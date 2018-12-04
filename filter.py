#!coding:utf-8
#  Created by bluebird on 2018/12/4
"""
docs
"""

from telegram.ext.filters import BaseFilter
from telegram.messageentity import MessageEntity
from urllib.parse import urlparse
from tool import check_ban_state, get_chat_data, get_user_data
from langdetect import detect
from datetime import datetime
from emoji import emoji_count

from constant import TELEGRAM_DOMAIN, BanMessageType, NUM_RE


class TelegramLink(BaseFilter):
    def filter(self, message):
        if not check_ban_state(message.chat_id, BanMessageType.TG_LINK):
            return False
        urls = message.parse_entities(types=MessageEntity.URL)
        if not len(urls):
            return False
        for url in urls.keys():
            if urlparse(url).netloc in TELEGRAM_DOMAIN:
                return True
        return False


class Lang(BaseFilter):
    def filter(self, message):
        chat_data: dict = get_chat_data(chat_id=message.chat_id)
        ban_list = chat_data.get(BanMessageType.LANG, default=False)
        if not ban_list:
            return False
        return detect(message.text) in ban_list


class Flood(BaseFilter):

    def filter(self, message):
        if not check_ban_state(message.chat_id, BanMessageType.FLOOD):
            return False
        chat_data: dict = get_chat_data(chat_id=message.chat_id)
        flood_limit = chat_data.get(BanMessageType.FLOOD, default={})
        time = flood_limit.get("time")
        num = flood_limit.get("num")
        if not time or not num:
            return
        now_time = datetime.now().timestamp()

        user_data = get_user_data(message.from_user.id)
        msg_data = user_data.get("msg_data", default=[])
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
        if emoji_count(message.text):
            return True
        return False


class Numbers(BaseFilter):
    def filter(self, message):
        if not check_ban_state(message.chat_id, BanMessageType.NUMBERS):
            return False
        return NUM_RE.search(message.text)
