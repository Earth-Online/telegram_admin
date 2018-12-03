#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from tool import command_wrap, messaage_warp


def test_command_wrap():
    """
    test command_wrap:
    """

    @command_wrap()
    def test_command():
        pass

    assert isinstance(test_command, CommandHandler)
    assert test_command.command == ["test_command"]

    @command_wrap(name="test")
    def test_command2():
        pass

    assert test_command2.command == ["test"]


def test_message_wrap():
    @messaage_warp(filters=Filters.all)
    def test_command():
        pass

    assert isinstance(test_command, MessageHandler)
    assert test_command.filters == Filters.all
