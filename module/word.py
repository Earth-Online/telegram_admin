#!coding:utf-8
#  Created by bluebird on 2018/12/13
"""
docs
"""
from sqlalchemy import Column, String, Boolean, INTEGER
from module import Base


class Sentence(Base):
    """
    telegarm user table
    """
    __tablename__ = 'sentence'

    sentence = Column(String(),primary_key=True)
    frequency = Column(INTEGER())

