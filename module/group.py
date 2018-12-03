#!coding:utf-8
#  Created by bluebird on 2018/12/4
"""
docs
"""
from sqlalchemy import Column, String
from module import Base


class Group(Base):
    """
    telegarm user table
    """
    __tablename__ = 'group'

    id = Column(String(20), primary_key=True)
    link = Column(String(50))
    title = Column(String(128))
