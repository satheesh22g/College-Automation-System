import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship,declarative_base
from sqlalchemy import create_engine
Base = declarative_base()

class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(String, primary_key=True)
    name = Column(String(250),nullable=False)
    user_type = Column(String(250), nullable=False)
    password = Column(String(250))
class Departments(Base):
    __tablename__ = 'departments'
    did = Column(Integer, primary_key=True)
    name = Column(String(30),nullable=False)
class CSE_Subjects():
    sub_id = Column(Integer, primary_key=True)
    sub_name = Column(Integer)
    dept_id = Column(Integer, ForeignKey('departments.did'))
    departments = relationship("Departments", foreign_keys=[dept_id])
    year = Column(Integer)
    sem = Column(Integer)
class Students(Base):
    __tablename__ = 'students'
    sid = Column(String, primary_key=True)
    sname = Column(String(30),nullable=False)
    dept_id = Column(Integer, ForeignKey('departments.did'))
    departments = relationship("Departments", foreign_keys=[dept_id])
class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(String, primary_key=True)
    name = Column(String(30),nullable=False)
    dept_id = Column(Integer, ForeignKey('departments.did'))
    departments = relationship("Departments", foreign_keys=[dept_id])
class Student_Profile(Base):
    __tablename__ = 'student_profile'
    sid = Column(String, primary_key=True)
    name = Column(String(30),nullable=False)
    branch = Column(String(30),nullable=False)
    year = Column(Integer)
    gender = Column(String(30),nullable=False)
    dob = Column(DateTime, nullable=True)
    entrance_type = Column(String(30))
    HorD = Column(String)
    dept_id = Column(Integer, ForeignKey('departments.did'))
    departments = relationship("Departments", foreign_keys=[dept_id])
    faculty_id = Column(String, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", foreign_keys=[faculty_id])
    
class Faculty_Profile(Base):
    __tablename__ = 'faculty_profile'
    id = Column(String, primary_key=True)
    name = Column(String(30),nullable=False)
    branch = Column(String(30),nullable=False)
    gender = Column(String(30))
    dob = Column(DateTime)
    phone = Column(Integer)
    dept_id = Column(Integer, ForeignKey('departments.did'))
    departments = relationship("Departments", foreign_keys=[dept_id])
    
class Marks(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    student_id = Column(String(30),ForeignKey('student_profile.sid'))
    name = Column(String(30))
    student_profile = relationship("Student_Profile", foreign_keys=[student_id])
    sub1 = Column(Integer)
    sub2 = Column(Integer)
    sub3 = Column(Integer)
    sub4 = Column(Integer)
    sub5 = Column(Integer)
    sub6 = Column(Integer)
    sub7 = Column(Integer)
    sub8 = Column(Integer)
    sub9 = Column(Integer)
    sub10 = Column(Integer)
    total = Column(Integer)
    average = Column(Integer)
    dept_id = Column(Integer, ForeignKey('departments.did'))
    departments = relationship("Departments", foreign_keys=[dept_id])
    year = Column(Integer)
    faculty_id = Column(String, ForeignKey('faculty.id'))
    councelor_id = Column(String, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", foreign_keys=[faculty_id])
    councelor = relationship("Faculty", foreign_keys=[councelor_id])
    sem = Column(Integer)
class Subjects(Base):
    __tablename__ = 'subjects'
    code = Column(String, primary_key=True)
    name = Column(String)
    sem = Column(String)
    dept_id = Column(Integer, ForeignKey('departments.did'))
    departments = relationship("Departments", foreign_keys=[dept_id])
    year = Column(Integer)
class Attendance(Base):
    __tablename__ = 'attendance'
    sid = Column(Integer, primary_key=True)
    #total_days = Column(Integer)
    student_id = Column(String, ForeignKey('student_profile.sid'))
    student_profile = relationship("Student_Profile", foreign_keys=[student_id]) 
    student_name = Column(String)
    sub1 = Column(Integer)
    sub2 = Column(Integer)
    sub3 = Column(Integer)
    sub4 = Column(Integer)
    sub5 = Column(Integer)
    sub6 = Column(Integer)
    sub7 = Column(Integer)
    sub8 = Column(Integer)
    sub9 = Column(Integer)
    sub10 = Column(Integer)
    sub11= Column(Integer)
    sub12 = Column(Integer)
    sub13 = Column(Integer)
    sub14 = Column(Integer)
    attend=Column(Integer)
    attend_perc = Column(Integer)
    dept_id = Column(Integer, ForeignKey('departments.did'))
    year = Column(Integer)
    departments = relationship("Departments", foreign_keys=[dept_id])
    faculty_id = Column(String, ForeignKey('faculty.id'))
    councelor_id = Column(String, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", foreign_keys=[faculty_id])
    councelor = relationship("Faculty", foreign_keys=[councelor_id])
    sem = Column(Integer)
    
class Faculty_Feedback(Base):
    __tablename__ = 'faculty_feedback'
    id = Column(Integer, primary_key=True)
    sub1 = Column(Integer)
    sub2 = Column(Integer)
    sub3 = Column(Integer)
    sub4 = Column(Integer)
    sub5 = Column(Integer)
    sub6 = Column(Integer)
    lab1 = Column(Integer)
    lab2 = Column(Integer)
    date = Column(DateTime)
    faculty_id = Column(String, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", foreign_keys=[faculty_id])
    student_id = Column(String, ForeignKey('student_profile.sid'),unique=True)
    student_profile = relationship("Student_Profile", foreign_keys=[student_id])
class Feedback(Base):
    __tablename__ = 'feedback'
    sid = Column(Integer, primary_key=True)
    name = Column(String(30))
    subject = Column(String(30),nullable=False)
    message = Column(String(300),nullable=False)
    user_id = Column(String(30), ForeignKey('accounts.id'))
    accounts = relationship("Accounts", foreign_keys=[user_id])
    

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
