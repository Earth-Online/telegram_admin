#!coding:utf-8
#  Created by bluebird on 2018/12/4
"""
docs
"""

from telegram.ext.filters import BaseFilter
from telegram.messageentity import MessageEntity
from urllib.parse import urlparse
from tool import check_ban_state, get_chat_data
from langdetect import detect

from constant import TELEGRAM_DOMAIN, BanMessageType


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
