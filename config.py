#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot config file
"""
import logging
import os


LOG_LEVEL = logging.INFO

TOKEN = os.environ.get('token') or ''

DB_URL = 'sqlite:///data/test.db'
