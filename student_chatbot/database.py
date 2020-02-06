import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(String, primary_key=True)
    name = Column(String(250),nullable=False)
    user_type = Column(String(250), nullable=False)
    password = Column(String(250))

class Marks(Base):
    __tablename__ = 'marks'
    sid = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    percent = Column(Integer)
    user_id = Column(String(30), ForeignKey('accounts.id'))
    


class Attendance(Base):
    __tablename__ = 'attendance'
    sid = Column(Integer, primary_key=True)
    name = Column(String(30),nullable=False)
    attend = Column(Integer,nullable=False)
    user_id = Column(String(30), ForeignKey('accounts.id'))

class Profile(Base):
    __tablename__ = 'profile'
    sid = Column(String, primary_key=True)
    name = Column(String(30),nullable=False)
    branch = Column(String(30),nullable=False)
    year = Column(Integer,nullable=False)
    gender = Column(String(30),nullable=False)
    phone = Column(Integer,nullable=False)
    user_id = Column(String(30), ForeignKey('accounts.id'))
class Feedback(Base):
    __tablename__ = 'feedback'
    sid = Column(Integer, primary_key=True)
    name = Column(String(30))
    subject = Column(String(30),nullable=False)
    message = Column(String(300),nullable=False)
    user_id = Column(String(30), ForeignKey('accounts.id'))

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
