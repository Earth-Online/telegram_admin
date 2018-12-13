#!coding:utf-8
#  Created by bluebird on 2018/12/13
"""
docs
"""
from sqlalchemy import Column, String, Boolean, INTEGER
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Sentence(Base):
    """
    telegarm user table
    """
    __tablename__ = 'sentence'

    sentence = Column(String())
    frequency = Column(INTEGER())

