# coding:utf-8
"""
bot database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_URL 
from .user import Base

Engine = create_engine(DB_URL)
DBSession = sessionmaker(bind=Engine)

Base.metadata.create_all(Engine)
