import sys
import csv
import os
from database import Base, Attendance, Marks, Accounts, Profile,Feedback
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from flask import Flask
app = Flask(__name__)
engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False},echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))
bcrypt = Bcrypt(app)
def attendance():
    f = open("attend.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid, name, attend in reader:
        db.execute("INSERT INTO attendance(sid, name, attend) VALUES(:i, :n, :a)", {"i": sid, "n": name, "a": attend})
    db.commit()

    print("attendance Completed ... ")
def admin():
    usern = '100'
    name = 'admin'
    usert = 'admin'
    passw = '1111'
    passw_hash = bcrypt.generate_password_hash(passw).decode('utf-8')
    db.execute("INSERT INTO accounts (id,name,user_type,password) VALUES (:u,:n,:t,:p)", {"u": usern,"n":name,"t":usert ,"p": passw_hash})
    db.commit()
'''
def student_profile():
    f = open("attend.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid, name, branch,year,gender,phone in reader:
        db.execute("INSERT INTO attendance(sid, name, branch,year,gender,phone) VALUES(:i, :n, :b,:y,:g,:p)", {"i": sid, "n": name, "b":branch,"y":year,"g":gender,"p":phone})
    db.commit()
    print("student profile Completed ... ")
def faculty_profile():
    f = open("attend.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid, name, branch,year,gender,phone in reader:
        db.execute("INSERT INTO attendance(sid, name, branch,year,gender,phone) VALUES(:i, :n, :b,:y,:g,:p)", {"i": sid, "n": name, "b":branch,"y":year,"g":gender,"p":phone})
    db.commit()
    print("faculty profile Completed ... ")
def hod_profile():
    f = open("attend.csv")
    reader = csv.reader(f)
    header = next(reader)
    print("Running script ... ")
    for sid, name, branch,year,gender,phone in reader:
        db.execute("INSERT INTO attendance(sid, name, branch,year,gender,phone) VALUES(:i, :n, :b,:y,:g,:p)", {"i": sid, "n": name, "b":branch,"y":year,"g":gender,"p":phone})
    db.commit()
    print("hod profile Completed ... ")'''

if __name__ == "__main__":
    attendance()
    '''student_profile()'''
    admin()
    