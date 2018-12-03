# coding:utf-8
"""
user table
"""
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    """
    telegarm user table
    """
    __tablename__ = 'user'

    # user_id
    id = Column(String(20), primary_key=True)
    isadmin = Column(Boolean, unique=False, default=False)
