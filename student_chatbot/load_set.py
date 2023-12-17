import sys
import csv
import os
from database import Base, Attendance, Marks, Accounts, Student_Profile,Feedback,Faculty_Feedback,Departments,Students,Faculty,Faculty_Profile
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

def department(session):
    departments_data = [
        {'did': 1, 'name': 'Civil Engineering'},
        {'did': 2, 'name': 'Electrical Engineering'},
        {'did': 3, 'name': 'Mechanical Engineering'},
        {'did': 4, 'name': 'Electronics and Communication Engineering'},
        {'did': 5, 'name': 'Computer Science and Engineering'}
    ]

    for data in departments_data:
        new_department = Departments(did=data['did'], name=data['name'])
        session.add(new_department)

    session.commit()
    print("Department insertion completed.")

def Student(session, filename='students.csv'):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        print("Running script...")
        for row in reader:
            sid, sname, dept_id = row
            new_student = Students(sid=sid, sname=sname, dept_id=dept_id)
            session.add(new_student)

        session.commit()
        print("Student insertion completed.")
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
    usern = 'ADMIN'
    name = 'admin'
    usert = 'admin'
    passw = 'srit'
    passw_hash = bcrypt.generate_password_hash(passw).decode('utf-8')
    db.execute("INSERT INTO accounts (id,name,user_type,password) VALUES (:u,:n,:t,:p)", {"u": usern,"n":name,"t":usert ,"p": passw_hash})
    db.commit()
    print("admin Completed ............................................ ")
def cse_clerk():
    usern = 'CLERK@CSE'
    name = 'CSE Clerk'
    usert = 'clerk'
    passw = 'srit'
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
    print("faculty Completed ............................................ ")
def cse_subjects():
    f = open("cse_subjects.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for code,name,sem,year,dept_id in reader:
        db.execute("INSERT INTO subjects (code,name,sem,year,dept_id) VALUES (:c,:n,:s,:y,:d)", {"c": code,"n":name,"s":sem, "y":year,"d":dept_id})
    db.commit()
    print("faculty Completed ............................................ ")

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
def cse2marks():
    f = open("cse2marks.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for student_id,name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,total,avg,dept_id,year,councelor_id,sem in reader:
        db.execute("INSERT INTO marks(student_id,name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,total,average,dept_id,year,councelor_id,sem) VALUES(:s,:n,:s1,:s2,:s3,:s4,:s5,:s6,:s7,:s8,:total,:avg,:d,:y,:c,:sem)", {"s":student_id,"n":name,"s1": sub1, "s2": sub2, "s3": sub3, "s4":sub4, "s5":sub5, "s6":sub6, "s7":sub7, "s8":sub8,"total":total,"avg":avg,"d":dept_id,  "y":year, "c":councelor_id,"sem":sem})
    db.commit()
    print("marks Completed .................................................... ")
def cse3marks():
    f = open("cse3marks2.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for student_id,name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,total,avg,dept_id,year,councelor_id,sem in reader:
        db.execute("INSERT INTO marks(student_id,name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,total,average,dept_id,year,councelor_id,sem) VALUES(:s,:n,:s1,:s2,:s3,:s4,:s5,:s6,:s7,:s8,:s9,:total,:avg,:d,:y,:c,:sem)", {"s":student_id,"n":name,"s1": sub1, "s2": sub2, "s3": sub3, "s4":sub4, "s5":sub5, "s6":sub6, "s7":sub7, "s8":sub8,"s9":sub9,"total":total,"avg":avg,"d":dept_id,  "y":year,"c":councelor_id,"sem":sem})
    db.commit()
    print("marks Completed .................................................... ")
def cse4marks():
    f = open("cse4marks.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for student_id,name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,total,avg,dept_id,year,councelor_id,sem in reader:
        db.execute("INSERT INTO marks(student_id,name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,total,average,dept_id,year,councelor_id,sem) VALUES(:s,:n,:s1,:s2,:s3,:s4,:s5,:s6,:s7,:s8,:total,:avg,:d,:y,:c,:sem)", {"s":student_id,"n":name,"s1": sub1, "s2": sub2, "s3": sub3, "s4":sub4, "s5":sub5, "s6":sub6, "s7":sub7, "s8":sub8,"total":total,"avg":avg,"d":dept_id,  "y":year,"c":councelor_id,"sem":sem})
    db.commit()
    print("marks Completed .................................................... ")
def _3cse_attendance():
    f = open("year3attendance.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,sub10,sub11,attend, attend_perc,dept_id,year,faculty_id,sem in reader:
        db.execute("INSERT INTO attendance(student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,sub10,sub11,attend, attend_perc,dept_id,year,councelor_id,sem) VALUES(:student_id,:student_name,:sub1,:sub2,:sub3,:sub4,:sub5,:sub6,:sub7,:sub8,:sub9,:sub10,:sub11,:attend, :attend_perc,:dept_id,:year,:faculty_id,:sem)", {"student_id":student_id,"student_name":student_name,"sub1":sub1,"sub2":sub2,"sub3":sub3,"sub4":sub4,"sub5":sub5,"sub6":sub6,"sub7":sub7,"sub8":sub8,"sub9":sub9,"sub10":sub10,"sub11":sub11,"attend":attend, "attend_perc":attend_perc,"dept_id":dept_id,"year":year,"faculty_id":faculty_id,"sem":sem})
    db.commit()
    print("attendance Completed ................................................ ")
def _2cse_attendance():
    f = open("year2attendance.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,attend, attend_perc,dept_id,year,faculty_id,sem in reader:
        db.execute("INSERT INTO attendance(student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,attend, attend_perc,dept_id,year,councelor_id,sem) VALUES(:student_id,:student_name,:sub1,:sub2,:sub3,:sub4,:sub5,:sub6,:sub7,:sub8,:sub9,:attend, :attend_perc,:dept_id,:year,:faculty_id,:sem)", {"student_id":student_id,"student_name":student_name,"sub1":sub1,"sub2":sub2,"sub3":sub3,"sub4":sub4,"sub5":sub5,"sub6":sub6,"sub7":sub7,"sub8":sub8,"sub9":sub9,"attend":attend, "attend_perc":attend_perc,"dept_id":dept_id,"year":year,"faculty_id":faculty_id,"sem":sem})
    db.commit()
def _4cse_attendance():
    f = open("year4attendance.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for student_id,student_name,sub1,sub2,sub3,sub4,attend, attend_perc,dept_id,year,faculty_id,sem in reader:
        db.execute("INSERT INTO attendance(student_id,student_name,sub1,sub2,sub3,sub4,attend, attend_perc,dept_id,year,councelor_id,sem) VALUES(:student_id,:student_name,:sub1,:sub2,:sub3,:sub4,:attend, :attend_perc,:dept_id,:year,:faculty_id,:sem)", {"student_id":student_id,"student_name":student_name,"sub1":sub1,"sub2":sub2,"sub3":sub3,"sub4":sub4,"attend":attend, "attend_perc":attend_perc,"dept_id":dept_id,"year":year,"faculty_id":faculty_id,"sem":sem})
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
    db.execute("delete from accounts")
    db.commit()
if __name__ == "__main__":
    department(db)
    Student(db,)
    #dummy()
    # department()
    # Faculty()
    # faculty_profile()
    admin()
    #cse_faculty_accounts()
    # cse_student_profile()
    # eee_student_profile()
    # ce_student_profile()
    # me_student_profile()
    # _3cse_attendance()
    # _4cse_attendance()
    # _2cse_attendance()
    # cse2marks()
    #cse3marks()
    # cse4marks()
    #cse_clerk()
    # cse_subjects()