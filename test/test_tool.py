#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""
from telegram.ext import CommandHandler
from tool import command_wrap


def test_command_command_wrap():
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
