# coding:utf-8
"""
bot database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL
from .user import Base
from .group import Group
from .word import Word

Engine = create_engine(DB_URL)
DBSession = sessionmaker(bind=Engine)

Base.metadata.create_all(Engine)
