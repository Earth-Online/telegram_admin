#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot config file
"""
import logging
import os


LOG_LEVEL = logging.DEBUG

# bot token
TOKEN = os.environ.get('token') or ''

# database url
DB_URL = 'sqlite:///data/test.db'

# firse admin
ADMIN = [529436356]
