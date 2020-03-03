import sys
import csv
import os
from database import Base, Attendance, Marks, Accounts, Student_Profile,Feedback,Departments,Students,Faculty,Faculty_Profile
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from flask import Flask
import pandas as pd
app = Flask(__name__)
engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False},echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))
bcrypt = Bcrypt(app)

def department():
    db.execute("INSERT INTO departments(did,name) VALUES(1,'Civil Engineering')")
    db.execute("INSERT INTO departments(did,name) VALUES(2,'Electrical Engineering')")
    db.execute("INSERT INTO departments(did,name) VALUES(3,'Mechanical Engineering')")
    db.execute("INSERT INTO departments(did,name) VALUES(4,'Electronics and Communication Engineering')")
    db.execute("INSERT INTO departments(did,name) VALUES(5,'Computer Science and Engineering')")
    db.commit()
    print("department Completed ................................ ")
def Student():
    f = open('students.csv')
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid, sname, dept_id in reader:
        db.execute("INSERT INTO students(sid, sname, dept_id) VALUES(:s, :n, :d)", {"s":sid, "n":sname, "d":dept_id })
    db.commit()
    print("students Completed .................................... ")

def Faculty():
    f = open('faculty.csv')
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for id, name, dept_id in reader:
        db.execute("INSERT INTO faculty(id, name, dept_id) VALUES(:s, :n, :d)", {"s":id, "n":name, "d":dept_id })
    db.commit()
    print("faculty Completed .................................... ")

def admin():
    usern = '100'
    name = 'admin'
    usert = 'admin'
    passw = '1111'
    passw_hash = bcrypt.generate_password_hash(passw).decode('utf-8')
    db.execute("INSERT INTO accounts (id,name,user_type,password) VALUES (:u,:n,:t,:p)", {"u": usern,"n":name,"t":usert ,"p": passw_hash})
    db.commit()
    print("admin Completed ............................................ ")
def cse_faculty_accounts():
    f = open("cse_faculty_accounts.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for id,name,user_type,password in reader:
        db.execute("INSERT INTO accounts (id,name,user_type,password) VALUES (:u,:n,:t,:p)", {"u": id,"n":name,"t":user_type ,"p": bcrypt.generate_password_hash(password).decode('utf-8')})
    db.commit()
    print("admin Completed ............................................ ")
def eee_student_profile():
    f = open("eee_students_profile.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,fact_id in reader:
        db.execute("INSERT INTO student_profile(sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,faculty_id) VALUES(:a, :b, :c,:d,:e,:f,:h,:i,:k,:l)", {"a":sid,"b": name,"c": branch,"d": year,"e": gender,"f": dob,"h": entrance_type,"i":HorD,"k":dept_id,"l":fact_id})
    db.commit()
def ece_student_profile():
    f = open("ece_students_profile.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,fact_id in reader:
        db.execute("INSERT INTO student_profile(sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,faculty_id) VALUES(:a, :b, :c,:d,:e,:f,:h,:i,:k,:l)", {"a":sid,"b": name,"c": branch,"d": year,"e": gender,"f": dob,"h": entrance_type,"i":HorD,"k":dept_id,"l":fact_id})
    db.commit()
def cse_student_profile():
    f = open("cse_students_profile.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,fact_id in reader:
        db.execute("INSERT INTO student_profile(sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,faculty_id) VALUES(:a, :b, :c,:d,:e,:f,:h,:i,:k,:l)", {"a":sid,"b": name,"c": branch,"d": year,"e": gender,"f": dob,"h": entrance_type,"i":HorD,"k":dept_id,"l":fact_id})
    db.commit()
def me_student_profile():
    f = open("me_students_profile.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,fact_id in reader:
        db.execute("INSERT INTO student_profile(sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,faculty_id) VALUES(:a, :b, :c,:d,:e,:f,:h,:i,:k,:l)", {"a":sid,"b": name,"c": branch,"d": year,"e": gender,"f": dob,"h": entrance_type,"i":HorD,"k":dept_id,"l":fact_id})
    db.commit()
def ce_student_profile():
    f = open("ce_students_profile.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,fact_id in reader:
        db.execute("INSERT INTO student_profile(sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,faculty_id) VALUES(:a, :b, :c,:d,:e,:f,:h,:i,:k,:l)", {"a":sid,"b": name,"c": branch,"d": year,"e": gender,"f": dob,"h": entrance_type,"i":HorD,"k":dept_id,"l":fact_id})
    db.commit()
    print("student profile Completed ........................................ ")
def Marks():
    f = open("marks.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for id,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,dept_id,student_id,year in reader:
        db.execute("INSERT INTO marks(id,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,dept_id,student_id,year) VALUES(:i,:s1,:s2,:s3,:s4,:s5,:s6,:s7,:s8,:d,:s,:y)", {"i":id,"s1": sub1, "s2": sub2, "s3": sub3, "s4":sub4, "s5":sub5, "s6":sub6, "s7":sub7, "s8":sub8,"d":dept_id, "s":student_id, "y":year})
    db.commit()
    print("marks Completed .................................................... ")
def cse_attendance():
    f = open("cse_3rd_Attendance.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid,student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,sub10,sub11,sub12,sub13,attend, attend_perc,dept_id,year,faculty_id in reader:
        db.execute("INSERT INTO attendance(sid,student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,sub10,sub11,sub12,sub13,attend, attend_perc,dept_id,year,faculty_id) VALUES(:sid,:student_id,:student_name,:sub1,:sub2,:sub3,:sub4,:sub5,:sub6,:sub7,:sub8,:sub9,:sub10,:sub11,:sub12,:sub13,:attend, :attend_perc,:dept_id,:year,:faculty_id)", {"sid":sid,"student_id":student_id,"student_name":student_name,"sub1":sub1,"sub2":sub2,"sub3":sub3,"sub4":sub4,"sub5":sub5,"sub6":sub6,"sub7":sub7,"sub8":sub8,"sub9":sub9,"sub10":sub10,"sub11":sub11,"sub12":sub12,"sub13":sub13,"attend":attend, "attend_perc":attend_perc,"dept_id":dept_id,"year":year,"faculty_id":faculty_id})
    db.commit()
    print("attendance Completed ................................................ ")

def faculty_profile():
    f = open("faculty_profile.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for id, name, branch,gender,dob,phone,dept_id in reader:
        db.execute("INSERT INTO faculty_profile(id, name, branch,gender,dob,phone,dept_id) VALUES(:i, :n, :b,:g,:d,:p,:d1)", {"i": id, "n": name, "b":branch,"g":gender,"d":dob,"p":phone,"d1":dept_id})
    db.commit()
    print("faculty profile Completed ... ")
'''
def hod_profile():
    f = open("attend.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid, name, branch,year,gender,phone in reader:
        db.execute("INSERT INTO attendance(sid, name, branch,year,gender,phone) VALUES(:i, :n, :b,:y,:g,:p)", {"i": sid, "n": name, "b":branch,"y":year,"g":gender,"p":phone})
    db.commit()
    print("hod profile Completed ... ")'''
def dummy():
    db.execute("DELETE FROM faculty_profile;")
    db.commit()
if __name__ == "__main__":
    #department()
    #Faculty()
    #faculty_profile()
    #admin()
    #cse_faculty_accounts()
    #cse_student_profile()
    #eee_student_profile()
    #ece_student_profile()
    #me_student_profile()
    #ce_student_profile()
    cse_attendance()
