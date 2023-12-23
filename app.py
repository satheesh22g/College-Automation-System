import os
import sys
from database import Base, Attendance, Marks, Accounts, Student_Profile,Feedback,Faculty_Feedback,Departments,Faculty,Faculty_Profile
from flask import send_file
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_session import Session
from database import Base, Attendance, Marks,Accounts, Student_Profile, Feedback,Departments,Faculty,Faculty_Profile, Faculty_Feedback
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.utils import secure_filename
from autocorrect import Speller
import docx2txt
import requests
import csv
import re
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sqlalchemy import create_engine, event
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sqlalchemy import text

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(24)

currentTime = datetime.now()
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db = DBSession()

# Define a function to disable bound value tracking
def disable_bound_value_tracking(dbapi_con, con_record):
    dbapi_con.execute('PRAGMA track_bound_values = OFF')

# Register the event to disable bound value tracking
event.listen(engine, 'connect', disable_bound_value_tracking)


# For autocorrect the input
spell = Speller(lang='en')
def str_to_class(str):
    return getattr(sys.modules[__name__], str)

@app.route("/")
def index():
    if 'user' not in session:
        return render_template("intro.html")
    else:
        return redirect(url_for('dashboard'))
# MAIN
@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    else:
        if session['usert']=="clerk":
            return render_template("clerk_menu.html")
        else:
            return render_template("menu.html")
@app.route("/query", methods=["GET","POST"])
def query_set():
    flash(session['namet'],"name")
    if request.method == 'GET':
        return render_template('query_set.html')
    try:
        if request.method == 'POST':
            msg=request.form.get("query").lower()
            ss=spell(msg)
            profile=db.execute(text("select sid from student_profile")).fetchall()
            profile_result=list([profile[i][0] for i in range(len(profile))])
            roll_flag = re.search("[1-9]{3}[a-zA-Z]{1}[0-9]{1}[a-zA-Z]{1}[0-9]{2}[0-9a-cA-C]{1}[0-9]{1}", ss)
            s="".join(re.findall("[1-9]{3}[a-zA-Z]{1}[0-9]{1}[a-zA-Z]{1}[0-9]{2}[0-9a-cA-C]{1}[0-9]{1}", ss))
            flash(msg, "success")
        if session['usert']=="Student":
            if "show my attendance" in ss:
                flash("Showing Result...", "error")
                return redirect(url_for('attendance'))
            if "show my marks" in ss:
                flash("Showing Result...", "error")
                return redirect(url_for('marks'))
            else:
                flash("Wrong! Try Again","error")
                print("error 1")
                return redirect(url_for('dashboard'))
        else:
            if (ss.split()[-1].upper() in profile_result) and re.search('profile', ss):
                flash("Showing Result...", "error")
                result=db.execute(text("SELECT * from student_profile where sid = :s;"),{"s":ss.split()[-1].upper()}).fetchall()
                attend=db.execute(text("SELECT * from attendance where student_id = :s;"),{"s":ss.split()[-1].upper()}).fetchall()
                marks=db.execute(text("SELECT * from marks where student_id = :s;"),{"s":ss.split()[-1].upper()}).fetchall()
                if result[0].year==4:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":4}).fetchall()
                if result[0].year==3:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":3}).fetchall()
                if result[0].year==2:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":2}).fetchall()
                print(19)
                return render_template("student_profile.html", results=result,marks=marks,attend=attend,sub=sub)

            # <----------------Queries for Count----------------------->
            if re.search('fail', ss) and re.search('how',ss) and re.search('many',ss) and re.search('year',ss) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss):
                result=db.execute(text("SELECT count(*) ,year,departments.name FROM marks INNER JOIN departments ON departments.did=marks.dept_id and (sub1<40 or sub2<40 or sub3<40 or sub4<40 or sub5<40 or sub6<40 or sub7<40 or sub8<40 or sub9<40) and year=:y;"),{"y":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                flash("Showing Result...", "error")
                print(1)
                return render_template("count_students.html", results=result)
            #how many students have less than 75 attendance in year 2
            if (re.search('attendance', ss) and re.search(r"0*[4-9]\d", ss) and re.search('how', ss) and re.search('many', ss) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss)) and re.search('less than',ss) or re.search('lessthan',ss) or re.search('<',ss):
                result=db.execute(text("SELECT count(*) ,year,departments.name FROM attendance INNER JOIN departments ON departments.did=attendance.dept_id and attend_perc<:a and year=:y;"),{"a":int("".join(re.findall(r"0*[4-9]\d", ss))),"y":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                flash("Showing Result...", "error")
                print(2)
                return render_template("count_students.html", results=result)
            # <----------------Queries for Graphs----------------------->
            if re.search('gra7ph', ss):
                flash("Showing Result...", "error")
                data = db.execute(text("select average from marks where year=:y"),{"y":4})
                df = pd.DataFrame(data)
                plt.plot(df)
                plt.show()
                plt.clf()
                print(3)
                return redirect(url_for('dashboard'))
            # show graph for marks of my counsel students
            if re.search('graph', ss) and (re.search('council', ss) or re.search('counsel', ss))and re.search('marks', ss):
                flash("Showing Result...", "error")
                data = db.execute(text("select round(average) from marks where councelor_id=:f"),{"f":session['user']})
                df = pd.DataFrame(data)
                plt.plot(df)
                plt.xlabel('Roll Numbers') 
                plt.ylabel('Percentage') 
                plt.savefig("static/graph")
                print(4)
                return render_template("graph.html")
            if re.search('compare', ss) and re.search('graph', ss) and re.search('year', ss) and re.search("(1|2|3|4)", ss) and re.search("subject", ss):
                lst=[]
                flash("Showing Result...", "error")
        
                s2 = db.execute(text("select average from marks where year=:y and sem=1"),{"y":int("".join(re.findall("(1|2|3|4)", ss)))})
                s1 = db.execute(text("select average from marks where year=:y and sem=2"),{"y":int("".join(re.findall("(1|2|3|4)", ss)))})
                df1 = pd.DataFrame(s1)
                plt.plot(df1,color='blue')
                df2 = pd.DataFrame(s2)
                plt.plot(df2,color='red')
                plt.xlabel('Subjects') 
                plt.ylabel('Marks') 
                #plt.show()
                plt.savefig("static/graph")
                print(555)
                return render_template("graph.html")
            if re.search('compare', ss) and re.search('graph', ss) and re.search('marks', ss) and roll_flag:
                lst=[]
                flash("Showing Result...", "error")
                s=ss.split()
                for i in s:
                    if re.search("[1-9]{3}[a-zA-Z]{1}[0-9]{1}[a-zA-Z]{1}[0-9]{2}[0-9a-cA-C]{1}[0-9]{1}", i):
                        lst.append("".join(re.findall("[1-9]{3}[a-zA-Z]{1}[0-9]{1}[a-zA-Z]{1}[0-9]{2}[0-9a-cA-C]{1}[0-9]{1}", i)))
                #s1 = db.execute("select sub1 from marks where councelor_id=:f",{"f":677})
                x = ['','Sub1','Sub2','Sub3','Sub4','Sub5','Sub6']
                s2 = db.execute(text("select sub1,sub2,sub3,sub4,sub5,sub6 from marks where student_id=:f"),{"f":lst[0].upper()})
                s1 = db.execute(text("select sub1,sub2,sub3,sub4,sub5,sub6 from marks where student_id=:f"),{"f":str(lst[1]).upper()})
                df1 = pd.DataFrame(s1)
                df2 = pd.DataFrame(s2)
                plt.style.use('classic')
                plt.plot(df1,label='s1', color='blue')
                plt.plot(df2,label='s2', color='red')
                plt.xlabel('Subjects') 
                plt.ylabel('Marks') 
                plt.savefig("static/graph")
                print(567)
                return render_template("graph.html")
            
            if re.search('compare', ss) and re.search('graph', ss) and re.search('marks', ss) and re.search('year', ss) and re.search("(1|2|3|4)", ss):
                
                flash("Showing Result...", "error")
                x = ['Sub1','Sub2','Sub3','Sub4','Sub5','Sub6','Sub7','Sub8']
                s2 = db.execute(text("select sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8 from marks where year=:y and sem=1"),{"y":int("".join(re.findall("(1|2|3|4)", ss)))})
                s1 = db.execute(text("select sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8 from marks where year=:y and sem=2"),{"y":int("".join(re.findall("(1|2|3|4)", ss)))})
                df1 = pd.DataFrame(s1)
                df2 = pd.DataFrame(s2)
                plt.style.use('classic')
                plt.plot(df1,label='s1', color='blue')
                plt.plot(df2,label='s2', color='red')
                plt.xlabel('Subjects') 
                plt.ylabel('Marks') 
                #plt.show()
                plt.savefig("static/graph")
                print(895)
                return render_template("graph.html")
            # <----------------Queries for Councel students----------------------->
            if (re.search('council', ss) or re.search('counsel', ss)) and re.search("student", ss) and re.search('show', ss):
                students=db.execute(text("select sid,name from student_profile where faculty_id=:f;"),{"f":int(session['user'])}).fetchall()
                attend = db.execute(text("select attend,attend_perc from attendance where councelor_id=:f;"),{"f":int(session['user'])}).fetchall()
                marks = db.execute(text("select average from marks where councelor_id=:f;"),{"f":session['user']}).fetchall()
                print(6)
                if len(attend):
                    flash("Showing Result...", "error")
                    return render_template("counsel_students.html", students=zip(students, attend,marks))
                else:
                    print("error 33")
                    flash("You don't have counseling students","error")
                    return redirect(url_for('dashboard'))
            # <----------------Queries for Attendance----------------------->
            
            if re.search('attendance', ss) and re.search('shortage',ss):
                flash("Showing Result...", "error")
                if session['usert']=="Faculty" or session['usert']=="counselor":
                    result=db.execute(text("select * from attendance where attend_perc<65 and councelor_id=:i"),{"i":session['user']}).fetchall()
                else:
                    result=db.execute(text("select * from attendance where attend_perc<65")).fetchall()
                print(8)
                return render_template("attendance.html",results=result)
            if session['usert']=="Faculty" or session['usert']=="counselor":
                if (re.search('attendance', ss) and re.search(r"0*[4-9]\d", ss) and (re.search('less than', ss) or re.search('lessthan', ss))) or (re.search('attendance', ss) and re.search("0*[4-9]\d", ss) and re.search('<', ss)):
                    flash("Showing Result...", "error")
                    result=db.execute(text("select * from attendance where attend_perc<:i and councelor_id=:j;"),{"i":int("".join(re.findall(r"0*[4-9]\d", ss))),"j":session['user']}).fetchall()
                    print(9)
                    return render_template("attendance.html",results=result)
                elif (re.search('attendance', ss) and re.search(r"0*[4-9]\d", ss) and (re.search('greater than', ss) or re.search('greaterthan', ss))) or (re.search('attendance', ss) and re.search("0*[4-9]\d", ss) and re.search('>', ss)):
                    flash("Showing Result...", "error")
                    result=db.execute(text("select * from attendance where attend_perc>:i and councelor_id=:j;"),{"i":int("".join(re.findall(r"0*[4-9]\d", ss))),"j":session['user']}).fetchall()
                    print(10)
                    return render_template("attendance.html",results=result)
            if re.search("[1-9]{3}[a-zA-Z]{1}[0-9]{1}[a-zA-Z]{1}[0-9]{2}[0-9a-cA-C]{1}[0-9]{1}", ss) and re.search('attendance', ss):
                flash("Showing Result...", "error")
                attend=db.execute(text("SELECT * from attendance where student_id =  :s;"),{"s":s.upper()}).fetchall()
                print(11)
                if attend:
                    return render_template("attendance.html", results=attend)
                else:
                    print("error 3")
                    flash("student not found","error")
                    return redirect(url_for('dashboard'))
            if re.search("[1-9]{3}[a-zA-Z]{1}[0-9]{1}[a-zA-Z]{1}[0-9]{2}[0-9a-cA-C]{1}[0-9]{1}", ss) and re.search('mark', ss):
                flash("Showing Result...", "error")
                attend=db.execute(text("SELECT * from marks where student_id =  :s;"),{"s":s.upper()}).fetchall()
                if attend[0].year==4:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":4}).fetchall()
                if attend[0].year==3:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":3}).fetchall()
                if attend[0].year==2:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":2}).fetchall()
                print(11)
                if attend:
                    return render_template("marks.html", results=attend,sub=sub)
                else:
                    print("error 3-1")
                    flash("student not found","error")
                    return redirect(url_for('dashboard'))
            if session['usert']=="HOD":
                if re.search('attendance', ss) and re.search("(1|2|3|4)", ss) and re.search('students', ss) and re.search('year', ss):
                    flash("Showing Result...", "error")
                    result=db.execute(text("select * from attendance where year=:i;"),{"i":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                    if result is not None:
                        print(12)
                        return render_template("attendance.html", results=result)
                    else:
                        print("error 3")
                        flash("Wrong! Try Again","error")
                        return redirect(url_for('dashboard'))
                if (re.search('attendance', ss) and re.search(r"0*[4-9]\d", ss) and (re.search('less than', ss) or re.search('lessthan', ss) or re.search('<', ss)) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss)):
                    flash("Showing Result...", "error")
                    result=db.execute(text("select * from attendance where attend_perc<:i and year=:y;"),{"i":int("".join(re.findall(r"0*[4-9]\d", ss))),"y":int("".join(re.findall(r'(?<![1-4])[1-4](?![1-4])', ss)))}).fetchall()
                    print(7)
                    return render_template("attendance.html",results=result)
                if (re.search('attendance', ss) and re.search(r"0*[4-9]\d", ss) and (re.search('greater than', ss) or re.search('greaterthan', ss) or re.search('>', ss)) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss)):
                    flash("Showing Result...", "error")
                    result=db.execute(text("select * from attendance where attend_perc> :i and year=:y;"),{"i":int("".join(re.findall(r"0*[4-9]\d", ss))),"y":int("".join(re.findall(r'(?<![1-4])[1-4](?![1-4])', ss)))}).fetchall()
                    print("7-1")
                    return render_template("attendance.html",results=result)
            if re.search('attendance', ss) and re.search('students', ss) and (re.search('council', ss) or re.search('counsel', ss)):
                flash("Showing Result...", "error")
                result=db.execute(text("select * from attendance where councelor_id=:j;"),{"j":session['user']}).fetchall()
                if result is not None:
                    print(12)
                    return render_template("attendance.html", results=result)
                else:
                    print("error 3")
                    flash("Wrong! Try Again","error")
                    return redirect(url_for('dashboard'))
            # <----------------Queries for Marks----------------------->
            if re.search('all', ss) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss) and re.search('year', ss) and re.search('clear',ss):
                flash("Showing Result...", "error")
                sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                result=db.execute(text("SELECT * FROM marks where (sub1>40 and sub2>40 and sub3>40 and sub4>40 and sub5>40 and sub6>40 and sub7>40 and sub8>40) and year=:y;"),{"y":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                print(13)
                return render_template("marks.html", results=result,sub=sub)
            if re.search('fail', ss) and re.search('year',ss) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss):
                flash("Showing Result...", "error")
                result=db.execute(text("SELECT * FROM marks where (sub1<40 or sub2<40 or sub3<40 or sub4<40 or sub5<40 or sub6<40 or sub7<40 or sub8<40 or sub9<40) and year=:y;"),{"y":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                print(14)
                return render_template("marks.html", results=result,sub=sub)
            if re.search('topper', ss) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss) and re.search('year', ss):
                flash("Showing Result...", "error")
                result=db.execute(text("SELECT *, max(average) from marks where dept_id=:d and year=:y"),{"d":5,"y":int("".join(re.findall(r'(?<![1-4])[1-4](?![1-4])', ss)))}).fetchall()
                sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                print(15)
                return render_template("marks.html", results=result,sub=sub)
            elif re.search('topper', ss) and (re.search('case',ss) or re.search('cse',ss)):
                flash("Showing Result...", "error")
                result=db.execute(text("SELECT *, max(average) from marks where dept_id=:d"),{"d":5}).fetchall()
                if result[0].year==4:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":4}).fetchall()
                if result[0].year==3:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":3}).fetchall()
                if result[0].year==2:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":2}).fetchall()
                print(18)
                return render_template("marks.html", results=result,sub=sub)
            if session['usert']=="HOD":
                if (re.search('marks', ss) or re.search('percentage', ss)) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss) and re.findall(r"0*[4-9]\d", ss) and (re.findall('less than', ss) or re.findall('lessthan', ss) or re.findall('<', ss)):
                    flash("Showing Result...", "error")
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                    result=db.execute(text("SELECT * from marks where year=:y and average<:a;"),{"y":int("".join(re.findall(r'(?<![0-9])[0-9](?![0-9])', ss))),"a":int("".join(re.findall(r"0*[4-9]\d", ss)))}).fetchall()
                    print(16)
                    return render_template("marks.html", results=result,sub=sub)
                if (re.search('marks', ss) or re.search('percentage', ss)) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss) and re.findall(r"0*[4-9]\d", ss) and (re.findall('greater than', ss) or re.findall('greaterthan', ss) or re.findall('>', ss)):
                    flash("Showing Result...", "error")
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                    result=db.execute(text("SELECT * from marks where year=:y and average>:a;"),{"y":int("".join(re.findall(r'(?<![0-9])[0-9](?![0-9])', ss))),"a":int("".join(re.findall(r"0*[4-9]\d", ss)))}).fetchall()
                    print(16)
                    return render_template("marks.html", results=result,sub=sub)
                if (re.search('marks', ss) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss) and re.search('year',ss)):
                    flash("Showing Result...", "error")
                    result=db.execute(text("SELECT * from marks where year=:y;"),{"y":int("".join(re.findall('(1|2|3|4)', ss)))}).fetchall()
                    print(17)
                    if result[0].year==4:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":4}).fetchall()
                    if result[0].year==3:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":3}).fetchall()
                    if result[0].year==2:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":2}).fetchall()
                    return render_template("marks.html", results=result,sub=sub)
            elif session['usert']=="Faculty" or session['usert']=="counselor":
                if (re.search('marks', ss) or re.search('percentage', ss)) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss) and re.findall(r"0*[4-9]\d", ss) and (re.findall('less than', ss) or re.findall('lessthan', ss) or re.findall('<', ss)):
                    flash("Showing Result...", "error")
                    result=db.execute(text("SELECT * from marks where councelor_id=:j and average<:a;"),{"j":session['user'],"a":int("".join(re.findall(r"0*[4-9]\d", ss)))}).fetchall()
                    print("16-1")
                    if result[0].year==4:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":4}).fetchall()
                    if result[0].year==3:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":3}).fetchall()
                    if result[0].year==2:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":2}).fetchall()
                    return render_template("marks.html", results=result,sub=sub)
                if (re.search('marks', ss) or re.search('percentage', ss)) and re.search(r'(?<![1-4])[1-4](?![1-4])', ss) and re.findall(r"0*[4-9]\d", ss) and (re.findall('greater than', ss) or re.findall('greaterthan', ss) or re.findall('>', ss)):
                    flash("Showing Result...", "error")
                    result=db.execute(text("SELECT * from marks where councelor_id=:j and average>:a;"),{"j":session['user'],"a":int("".join(re.findall(r"0*[4-9]\d", ss)))}).fetchall()
                    print("16-2")
                    if result[0].year==4:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":4}).fetchall()
                    if result[0].year==3:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":3}).fetchall()
                    if result[0].year==2:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":2}).fetchall()
                    return render_template("marks.html", results=result,sub=sub)
                if (re.search('marks', ss) and re.search('student', ss)):
                    flash("Showing Result...", "error")
                    result=db.execute(text("SELECT * from marks where councelor_id=:j;"),{"j":session['user']}).fetchall()
                    print("17-1")
                    if result[0].year==4:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":4}).fetchall()
                    if result[0].year==3:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":3}).fetchall()
                    if result[0].year==2:
                        sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":2}).fetchall()
                    return render_template("marks.html", results=result,sub=sub)
                if re.search('fail', ss) and re.search('how',ss) and re.search('many',ss):
                    result=db.execute(text("SELECT count(*) ,year,departments.name FROM marks INNER JOIN departments ON departments.did=marks.dept_id and (sub1<40 or sub2<40 or sub3<40 or sub4<40 or sub5<40 or sub6<40 or sub7<40 or sub8<40 or sub9<40) and councelor_id=:y;"),{"y":session['user']}).fetchall()
                    flash("Showing Result...", "error")
                    print("1-1")
                    return render_template("count_students.html", results=result)
            
            # <----------------Queries for Profile----------------------->
            if (ss.split()[-1].upper() in profile_result) and re.search('profile', ss):
                flash("Showing Result...", "error")
                result=db.execute(text("SELECT * from student_profile where sid = :s;"),{"s":ss.split()[-1].upper()}).fetchall()
                attend=db.execute(text("SELECT * from attendance where student_id = :s;"),{"s":ss.split()[-1].upper()}).fetchall()
                marks=db.execute(text("SELECT * from marks where student_id = :s;"),{"s":ss.split()[-1].upper()}).fetchall()
                if result[0].year==4:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":4}).fetchall()
                if result[0].year==3:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":3}).fetchall()
                if result[0].year==2:
                    sub = db.execute(text('select name,sem from subjects where year=:y and sem like "%_1"'),{"y":2}).fetchall()
                print(19)
                return render_template("student_profile.html", results=result,marks=marks,attend=attend,sub=sub)
                
            else:
                print("error 6",ss,session['usert'])
                flash("Wrong! Try Again","error")
                return redirect(url_for('query_set'))
    except:
        flash("Input out of range","error")
        print(ss)
        print("error 7")
        return redirect(url_for('query_set')) 
    print(999) 
    flash("I'm not Understanding🤔! Try Again","error")
    return redirect(url_for('dashboard'))  
@app.route("/<sid>/Council-Students")
def council_students(sid):
    res=db.execute(text("SELECT * FROM student_profile WHERE sid = :u"), {"u": sid}).fetchall()
    attend=db.execute(text("SELECT * from attendance where student_id = :s;"),{"s":sid}).fetchall()
    marks=db.execute(text("SELECT * from marks where student_id = :s;"),{"s":sid}).fetchall()
    return render_template("student_profile.html",results=res,marks=marks,attend=attend)
@app.route("/profile")
def profile():
    if session['usert']=="Student":
        res = db.query(Student_Profile).filter_by(sid=session['user']).all()
        attend = db.query(Attendance).filter_by(student_id=session['user']).all()
        marks = db.query(Marks).filter_by(student_id=session['user']).all()
        return render_template("student_profile.html",results=res,marks=marks,attend=attend)
    else:
        user_id = session['user']
        res=db.query(Faculty_Profile).filter_by(id=user_id).all()
        return render_template("faculty_profile.html",results=res)
@app.route("/attendance")
def attendance():
    user_id = session['user']  # Assuming session['user'] holds the value for student_id
    result = db.query(Attendance).filter_by(student_id=user_id).all()
    return render_template("attendance.html",results=result)

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/marks")
def marks():
    user_id = session['user'] 
    result = db.query(Marks).filter_by(student_id=user_id).all()
    return render_template("marks.html",results=result)
@app.route("/attendance_display")
def attendance_update():
    return render_template("attendance_form.html")

@app.route("/suggestions", methods=["GET", "POST"])
def Suggestions():
    # today_date = datetime.today()  # Calculate today's date outside the lambda

    # too_old = today_date - timedelta(days=1)
    # print('too_old',too_old)
    # # Delete older feedback entries
    # db.query(Faculty_Feedback).filter(Faculty_Feedback.date <= too_old).delete()

    msg1 = msg2 = ""
    try:
        if request.method == "POST":
            name = request.form.get("name")
            subject = request.form.get("subject")
            message = request.form.get("message")

            # Insert new feedback using parameterized query
            new_feedback = Feedback(name=name, subject=subject, message=message, user_id=session['user'])
            db.add(new_feedback)
            db.commit()
            msg1 = "Submitted!"
            msg2 = "Thank you for your feedback"

    except IntegrityError:
        message = "Roll Number already exists."
        # Perform rollback if an IntegrityError occurs
        db.rollback()

    return render_template("feedback.html", msg1=msg1, msg2=msg2)

# Faculty Feedback
@app.route("/Faculty-Feedback", methods=["GET", "POST"])
def Faculty_Feedback():
    too_old = datetime.today() - timedelta(days=1)
    db.query(Faculty_Feedback).filter(Faculty_Feedback.date <= too_old).delete()
    db.commit()
    msg1 = msg2 = ""
    try:
        if request.method == "POST":
            sub1 = request.form.get("sub1")
            sub2 = request.form.get("sub2")
            sub3 = request.form.get("sub3")
            sub4 = request.form.get("sub4")
            sub5 = request.form.get("sub5")
            sub6 = request.form.get("sub6")
            lab1 = request.form.get("lab1")
            lab2 = request.form.get("lab2")
            result1 = db.execute(text("INSERT INTO faculty_feedback (sub1, sub2, sub3, sub4, sub5, sub6, lab1, lab2, date, student_id) VALUES (:sub1, :sub2, :sub3, :sub4, :sub5, :sub6, :lab1, :lab2, :date, :s)"), {"sub1": sub1, "sub2": sub2, "sub3": sub3, "sub4": sub4, "sub5": sub5, "sub6": sub6, "lab1": lab1, "lab2": lab2, "date": datetime.datetime.today(), "s": session['user']})
            db.commit()
            new_feedback = Faculty_Feedback(
                sub1=sub1,
                sub2=sub2,
                sub3=sub3,
                sub4=sub4,
                sub5=sub5,
                sub6=sub6,
                lab1=lab1,
                lab2=lab2,
                date=datetime.today(),
                student_id=session['user']
            )

            # Add the new_feedback object to the session
            db.add(new_feedback)

            # Commit the changes
            db.commit()
            msg1 = "Submitted!"
            msg2 = "Thank You for your Feedback"
    except exc.IntegrityError:
        msg1 = "Already Submitted."
        db.rollback()
        db.commit()
    return render_template("feedback.html", msg1=msg1, msg2=msg2)

# To display all the complaints to the admin
@app.route("/adminfeedbacks")
def adminfeedbacks():
    result=db.query(Feedback).all()
    return render_template('feedback.html',result=result)
@app.route("/feedbacks")
def show_feedback():
    # display FeedBack  To HOD
    result = db.query(Faculty_Feedback).all()
    return render_template('show_feedback.html',res=result)
@app.route('/<data>/download')
def download_file(data):
    s=db.execute(data).fetchall()
    df = pd.DataFrame(list(s))
    writer = pd.ExcelWriter('outputt.xlsx')
    df.to_excel(writer,sheet_name="lkjhgf")
    x=writer.save()
    return send_file('outputt.xlsx', as_attachment=True,mimetype='.xlsx')

@app.route("/admin-updates", methods=["GET", "POST"])
def admin_update():
    faculty_list=db.execute(text('select * from faculty')).fetchall()
    if request.method == "POST":
        dept_id = request.form.get('dept_id')
        faculty = (request.form.get('faculty'))
        table = request.form['name']
        try: 
            file1 = request.files['file']
            filename = secure_filename(file1.filename)
            ext = os.path.splitext(filename)[-1].lower()
            if ext == ".xlsx":
                read_file = pd.read_excel(filename)
                read_file.to_csv("o.csv", index = None, header=True)
                f = open("o.csv")
            elif ext ==".csv":
                f = open(filename)
            else:
                output = "is an unknown file format."
                return render_template('admin_updates.html', output=output,flist=faculty_list)
            
            reader = csv.reader(f)
            try:
                if table=="Attendance":
                    for attend, dept_id,year,student_id in reader:
                        db.execute(text("INSERT INTO attendance(attend,dept_id,year,student_id) VALUES(:a, :d, :y, :s)"), { "a": attend, "d":dept_id, "y":year, "s":student_id })
                    db.commit()
                    return redirect(url_for('dashboard'))
                elif table=="Marks":
                    for id,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,dept_id,student_id,year in reader:
                        db.execute(text("INSERT INTO marks(id,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,dept_id,student_id,year) VALUES(:i,:s1,:s2,:s3,:s4,:s5,:s6,:s7,:s8,:d,:s,:y)"), {"i":id,"s1": sub1, "s2": sub2, "s3": sub3, "s4":sub4, "s5":sub5, "s6":sub6, "s7":sub7, "s8":sub8,"d":dept_id, "s":student_id, "y":year})
                    db.commit()
                elif table=="Profile":
                    for sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,fact_id in reader:
                        db.execute(text("INSERT INTO student_profile(sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,faculty_id) VALUES(:a, :b, :c,:d,:e,:f,:h,:i,:k,:l)"), {"a":sid,"b": name,"c": branch,"d": year,"e": gender,"f": dob,"h": entrance_type,"i":HorD,"k":dept_id,"l":fact_id})
                    db.commit()
                elif table=="Faculty":
                    for id, name, dept_id in reader:
                        db.execute(text("INSERT INTO faculty(id, name, dept_id) VALUES(:s, :n, :d)"), {"s":id, "n":name, "d":dept_id })
                    db.commit()
            except:
                message = "columns must be in correct order {}".format(str_to_class-olumns.keys())
                return render_template('admin_updates.html', output=message,flist=faculty_list)
        except exc.SQLAlchemyError:
            message = "columns must be in correct order {}".format(str_to_class(table).__table__.columns.keys())
            return render_template('admin_updates.html', output=message,flist=faculty_list)
    
    return render_template("admin_updates.html",flist=faculty_list)
@app.route("/load-data", methods=["GET", "POST"])
def load_data():
    faculty_list=db.execute(text('select * from faculty')).fetchall()
    if request.method == "POST":
        dept_id = request.form.get('dept_id')
        faculty_id = request.form.get('faculty')
        year = request.form.get('year')
        table = request.form['table']
        try: 
            file1 = request.files['file']
            filename = secure_filename(file1.filename)
            ext = os.path.splitext(filename)[-1].lower()
            if ext == ".xlsx":
                read_file = pd.read_excel(filename)
                read_file.to_csv("o.csv", index = None, header=True)
                f = open("o.csv")
            elif ext ==".csv":
                f = open(filename)
            else:
                output = "is an unknown file format."
                return render_template('load_data.html', output=output,flist=faculty_list)
            
            reader = csv.reader(f)
            try:
                if table=="Attendance":
                    if year=="4":
                        for student_id,student_name,sub1,sub2,sub3,sub4,attend, attend_perc in reader:
                            db.execute(text("INSERT INTO attendance(student_id,student_name,sub1,sub2,sub3,sub4,attend, attend_perc,dept_id,year,faculty_id) VALUES(:student_id,:student_name,:sub1,:sub2,:sub3,:sub4,:attend, :attend_perc,:dept_id,:year,:faculty_id)"), {"student_id":student_id,"student_name":student_name,"sub1":sub1,"sub2":sub2,"sub3":sub3,"sub4":sub4,"attend":attend, "attend_perc":attend_perc,"dept_id":dept_id,"year":year,"faculty_id":faculty_id})
                        db.commit()
                        return redirect(url_for('dashboard'))
                    elif year=="3":
                        for student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,sub10,sub11,attend, attend_perc in reader:
                            db.execute(text("INSERT INTO attendance(student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,sub10,sub11,attend, attend_perc,dept_id,year,faculty_id) VALUES(:student_id,:student_name,:sub1,:sub2,:sub3,:sub4,:sub5,:sub6,:sub7,:sub8,:sub9,:sub10,:sub11,:attend, :attend_perc,:dept_id,:year,:faculty_id)"), {"student_id":student_id,"student_name":student_name,"sub1":sub1,"sub2":sub2,"sub3":sub3,"sub4":sub4,"sub5":sub5,"sub6":sub6,"sub7":sub7,"sub8":sub8,"sub9":sub9,"sub10":sub10,"sub11":sub11,"attend":attend, "attend_perc":attend_perc,"dept_id":dept_id,"year":year,"faculty_id":faculty_id})
                        db.commit()
                    elif year=="2":
                        for student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,attend, attend_perc,dept_id,year,faculty_id in reader:
                            db.execute(("INSERT INTO attendance(student_id,student_name,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,attend, attend_perc,dept_id,year,councelor_id) VALUES(:student_id,:student_name,:sub1,:sub2,:sub3,:sub4,:sub5,:sub6,:sub7,:sub8,:sub9,:attend, :attend_perc,:dept_id,:year,:faculty_id)"), {"student_id":student_id,"student_name":student_name,"sub1":sub1,"sub2":sub2,"sub3":sub3,"sub4":sub4,"sub5":sub5,"sub6":sub6,"sub7":sub7,"sub8":sub8,"sub9":sub9,"attend":attend, "attend_perc":attend_perc,"dept_id":dept_id,"year":year,"faculty_id":faculty_id})
                            db.commit()
                elif table=="Marks":
                    for id,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,dept_id,student_id,year in reader:
                        db.execute(("INSERT INTO marks(id,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,dept_id,student_id,year) VALUES(:i,:s1,:s2,:s3,:s4,:s5,:s6,:s7,:s8,:d,:s,:y)"), {"i":id,"s1": sub1, "s2": sub2, "s3": sub3, "s4":sub4, "s5":sub5, "s6":sub6, "s7":sub7, "s8":sub8,"d":dept_id, "s":student_id, "y":year})
                    db.commit()
                elif table=="Profile":
                    for sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,fact_id in reader:
                        db.execute(text("INSERT INTO student_profile(sid,name,branch,year,gender,dob,entrance_type,HorD,dept_id,faculty_id) VALUES(:a, :b, :c,:d,:e,:f,:h,:i,:k,:l)"), {"a":sid,"b": name,"c": branch,"d": year,"e": gender,"f": dob,"h": entrance_type,"i":HorD,"k":dept_id,"l":fact_id})
                    db.commit()
                elif table=="Faculty":
                    for id, name, dept_id in reader:
                        db.execute(text("INSERT INTO faculty(id, name, dept_id) VALUES(:s, :n, :d)"), {"s":id, "n":name, "d":dept_id })
                    db.commit()
            except:
                message = "columns must be in correct order {}".format(str_to_class(table).__table__.columns.keys())
                return render_template('load_data.html', output=message,flist=faculty_list)
        except exc.SQLAlchemyError:
            message = "columns must be in correct order {}".format(str_to_class(table).__table__.columns.keys())
            return render_template('load_data.html', output=message,flist=faculty_list)
    
    return render_template("load_data.html",flist=faculty_list)
# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    message = ""

    if request.method == "POST":
        try: 
            usern = request.form.get("username").upper()
            name = request.form.get("name")
            usert = request.form.get("usertyp")
            passw = request.form.get("password")
            passw_hash = bcrypt.generate_password_hash(passw).decode('utf-8')
            result = Accounts(id=usern, name=name, user_type=usert, password=passw_hash)
            db.add(result)
            db.commit()
            if result is not None:
                session['user'] = usern
                session['namet'] = name
                session['usert'] = usert
                flash("Your successfully Registrated",'alert')
                return redirect(url_for('dashboard'))
        except exc.IntegrityError:
            message = "Roll Number already exists."
            db.rollback()
            db.commit()
    return render_template("registration.html", message=message)

# Change Pasword
@app.route("/change-password", methods=["GET", "POST"])
def changepass():
    if 'user' not in session:
        return redirect(url_for('login'))
    msg=""
    if request.method == "POST":
        try:
            epswd = request.form.get("epassword")
            cpswd = request.form.get("cpassword")
            passw_hash = bcrypt.generate_password_hash(cpswd).decode('utf-8')
            exist = db.query(Accounts).filter_by(id = session['user']).first()
            if bcrypt.check_password_hash(exist.password, epswd) is True:
                exist.password = passw_hash
                db.commit()
                flash("Password Changed Successfully","alert")
                return redirect(url_for('dashboard'))
        except exc.IntegrityError:
            msg = "Unable to process try again"
        msg="Existing Not matching"
    return render_template("change_password.html",m=msg)

# Reset
@app.route("/reset", methods=["GET", "POST"])
def reset():
    msg=""
    if session['usert']=="admin":
        
        if request.method == "POST":
            rollno = request.form.get("rollno")
            passw_hash = bcrypt.generate_password_hash("srit").decode('utf-8')
            res = db.query(Accounts).filter_by(id=rollno).first()
            res.password = passw_hash
            db.commit()
            if res is not None:
                flash("Password Reset Successfully","alert")
                return redirect(url_for('dashboard'))
        msg=""
        return render_template("pswdreset.html",m=msg)
    else:
        return redirect(url_for('dashboard'))
# LOGOUT
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('dashboard'))
# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    message = ""
    if request.method == "POST":
        usern = request.form.get("username").upper()
        passw = request.form.get("password").encode('utf-8')
        result = db.query(Accounts).filter_by(id=usern).first()
        if result is not None:
            if bcrypt.check_password_hash(result.password, passw) is True:
                session['user'] = usern
                session['namet'] = result.name
                session['usert'] = result.user_type
                flash("Hello  "+result.name+" !","greet")
                return redirect(url_for('dashboard'))
        message = "Username or password is incorrect."
    return render_template("login.html", message=message)

# Main
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8008)
