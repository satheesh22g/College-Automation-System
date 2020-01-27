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
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False,unique=True)
    user_type = Column(String(250), nullable=False)
    password = Column(String(250))

class Marks(Base):
    __tablename__ = 'marks'
    s_id = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    percent = Column(Integer)
    


class Attendance(Base):
    __tablename__ = 'attendance'
    sid = Column(Integer, primary_key=True)
    name = Column(String(30),nullable=False)
    attend = Column(Integer,nullable=False)

class Profile(Base):
    __tablename__ = 'profile'
    sid = Column(Integer, primary_key=True)
    name = Column(String(30),nullable=False)
    branch = Column(String(30),nullable=False)
    year = Column(Integer,nullable=False)
    gender = Column(String(30),nullable=False)
    phone = Column(Integer,nullable=False)
    
    
'''class Reviews(Base):
    __tablename__ = 'reviews'

   
    id = Column(Integer, primary_key=True)
    acc_id = Column(String(30),nullable=False)
    book_id = Column(String(50),nullable=False)
    comment = Column(String(30),nullable=False)
    rating = Column(Integer,nullable=False)
    date= Column(DateTime)
    reviews_acc_id_fkey = Column(Integer, ForeignKey('accounts.id'))
    accounts = relationship(Accounts)
    reviews_book_id_fkey = Column(Integer, ForeignKey('books.id'))
    books = relationship(Books)
    '''
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
