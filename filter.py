#!coding:utf-8
#  Created by bluebird on 2018/12/4
"""
docs
"""

from telegram.ext.filters import BaseFilter
from telegram.messageentity import MessageEntity
from urllib.parse import urlparse
from tool import check_ban_state

from constant import TELEGRAM_DOMAIN, MessageType


class TelegramLink(BaseFilter):
    def filter(self, message):
        if not check_ban_state(message.chat_id, MessageType.TG_LINK):
            return False
        urls = message.parse_entities(types=MessageEntity.URL)
        if not len(urls):
            return False
        for url in urls.keys():
            if urlparse(url).netloc in TELEGRAM_DOMAIN:
                return True
        return False
