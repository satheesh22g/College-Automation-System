import os
import sys
from flask import send_file
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_session import Session
from database import Base, Attendance, Marks,Accounts, Student_Profile, Feedback,Students,Departments,Faculty,Faculty_Profile
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.utils import secure_filename
import docx2txt
import requests
import csv
import re
import pandas as pd
import matplotlib.pyplot as plt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(24)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False},echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))

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
        return render_template("menu.html")


@app.route("/query", methods=["POST"])
def quer():
    try:

        
        if request.method == 'POST':
            ss=request.form.get("msg").lower()
            profile=db.execute("select sid from student_profile").fetchall()
            profile_result=list([profile[i][0] for i in range(len(profile))])
            roll_flag = re.search("[1-9]{3}[a-zA-Z]{1}[0-9]{1}[a-zA-Z]{1}[0-9]{2}[0-9a-cA-C]{1}[0-9]{1}$", ss)
            s="".join(re.findall("[1-9]{3}[a-zA-Z]{1}[0-9]{1}[a-zA-Z]{1}[0-9]{2}[0-9a-cA-C]{1}[0-9]{1}$", ss))
        if session['usert']=="Student":
            if "show my attendance" in ss:
                return redirect(url_for('attendance'))
            else:
                flash("Wrong! Try Again")
                return redirect(url_for('dashboard'))
        else:
            if "show graph" in ss:
                return redirect(url_for('plot_graph'))
            if re.search('attendance', ss) and re.search("(1|2|3|4)", ss) and re.search('students', ss) and re.search('year', ss):
                result=db.execute("select * from attendance where year=:i;",{"i":int("".join(re.findall("(1|2|3|4)", ss)))}).fetchall()
                if result is not None:
                    return render_template("attendance.html", results=result)
                else:
                    flash("Wrong! Try Again")
                    return redirect(url_for('dashboard'))
            if "marks" in ss:
                result=db.execute("select *,(sub1+sub2+sub3+sub4+sub5+sub6+sub7+sub8) as total,(sub1+sub2+sub3+sub4+sub5+sub6+sub7+sub8)/8 as avg from marks where avg<60;").fetchall()
                return render_template("marks.html", results=result)
            if re.search('attendance shortage', ss):
                result=db.execute("select * from attendance where attend_perc<65").fetchall()
                return render_template("attendance.html",results=result)
            if (re.search('attendance', ss) and re.search(r"0*[4-9]\d", ss) and (re.search('less than', ss) or re.search('lessthan', ss))) or (re.search('attendance', ss) and re.search("0*[4-9]\d", ss) and re.search('<', ss)):
                result=db.execute("select * from attendance where attend_perc<:i;",{"i":int("".join(re.findall(r"0*[4-9]\d", ss)))}).fetchall()
                return render_template("attendance.html",results=result)
            if (re.search('attendance', ss) and re.search(r"0*[4-9]\d", ss) and (re.search('greater than', ss) or re.search('greaterthan', ss))) or (re.search('attendance', ss) and re.search("0*[4-9]\d", ss) and re.search('>', ss)):
                result=db.execute("select * from attendance where attend_perc>:i;",{"i":int("".join(re.findall(r"0*[4-9]\d", ss)))}).fetchall()
                return render_template("attendance.html",results=result)
            elif (ss.split()[-1].upper() in profile_result) and re.search('profile', ss):
                result=db.execute("SELECT * from student_profile where sid =  :s;",{"s":ss.split()[-1].upper()})
                attend=db.execute("SELECT * from attendance where student_id =  :s;",{"s":ss.split()[-1].upper()})
                marks=db.execute("SELECT * from marks where student_id =  :s;",{"s":ss.split()[-1].upper()})
                return render_template("student_profile.html", results=result,marks=marks,attend=attend)
            elif roll_flag and re.search('attendance', ss):
                attend=db.execute("SELECT * from attendance where student_id =  :s;",{"s":s.upper()})
                return render_template("attendance.html", results=attend)
            else:
                flash("Wrong! Try Again")
                return redirect(url_for('dashboard'))
    except:
        flash("Input out of range")
    return redirect(url_for('dashboard'))
    

@app.route("/profile")
def profile():
    if session['usert']=="Student":
        res=db.execute("SELECT * FROM student_profile WHERE sid = :u", {"u": session['user']}).fetchall()
        return render_template("student_profile.html",results=res)
    else:
        res=db.execute("SELECT * FROM Faculty_Profile WHERE id = :u", {"u": session['user']}).fetchall()
        return render_template("faculty_profile.html",results=res)
@app.route("/attendance")
def attendance():
    result=db.execute("SELECT * FROM attendance WHERE sid = :u", {"u": session['user']}).fetchall()
    return render_template("attendance.html",results=result)

@app.route("/marks")
def marks():
    return render_template("marks.html")
@app.route("/attendance_display")
def attendance_update():
    return render_template("attendance_form.html")
@app.route("/suggestions", methods=["GET", "POST"])
def Suggestions():
    msg1=msg2=""
    try:
        if request.method == "POST":
            sid = request.form.get("sid")
            name = request.form.get("name")
            subject = request.form.get("subject")
            message = request.form.get("message")
            result = db.execute("INSERT INTO feedback (name,subject,message,user_id) VALUES (:n,:s,:m,:u)", {"n":name,"s":subject ,"m": message,"u":session['user']})
            db.commit()
            msg1= "Submitted!"
            msg2 = "Thank You for your Feedback"
    except exc.IntegrityError:
            message = "Roll Number already exists."
            db.execute("ROLLBACK")
            db.commit()
    return render_template("feedback.html",msg1=msg1,msg2=msg2)

# To display all the complaints to the admin
@app.route("/adminfeedbacks")
def adminfeedbacks():
    result=db.execute("SELECT * FROM feedback").fetchall()
    return render_template('feedback.html',result=result)

@app.route("/graphs")
def plot_graph():
    result=db.execute("SELECT sid,attend FROM attendance WHERE attend < 75 ORDER BY sid").fetchall()
    x=["sart","ygf"]
    y=[]
    for i,j in result:
        y.append(j)
    plt.plot(x,y)
    
    d="sath"
    plt.title(d)
    plt.xlabel(d, fontsize=18)
    plt.ylabel(d, fontsize=16)
    plt.savefig('static/graph.png')
    return render_template('graphs.html',result=result)
@app.route('/download')
def download_file():
    s=db.execute("select * from student_profile").fetchall()
    df = pd.DataFrame(list(s))
    writer = pd.ExcelWriter('outputt.xlsx')
    df.to_excel(writer,sheet_name="lkjhgf")
    x=writer.save()
    return send_file('outputt.xlsx', as_attachment=True,mimetype='.xlsx')

@app.route("/admin-updates", methods=["GET", "POST"])
def admin_update():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert']=="admin":
        dept_id = request.form.get('dept_id')
        try:
            if request.method == "POST":
                
                faculty_list=db.execute("select * from faculty where dept_id=:i",{"i":dept_id}).fetchall()
                table = request.form.get('table')
                return redirect(url_for('dashboard'))
        except:
            message = "error"
            return render_template("admin_updates.html",msg=message)
        return render_template("admin_updates.html")
    else:
        return redirect(url_for('dashboard'))
    return render_template("admin_updates.html",flist=faculty_list)
@app.route("/load-data", methods=["GET", "POST"])
def load_data():
    if request.method == "POST":
        dept_id = request.form.get('dept_id')
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
                return render_template('load_data.html', output=output)
            
            reader = csv.reader(f)
            try:
                if table=="Attendance":
                    for attend, dept_id,year,student_id in reader:
                        db.execute("INSERT INTO attendance(attend,dept_id,year,student_id) VALUES(:a, :d, :y, :s)", { "a": attend, "d":dept_id, "y":year, "s":student_id })
                    db.commit()
                    return redirect(url_for('dashboard'))
                elif table=="Marks":
                    for id,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,dept_id,student_id,year in reader:
                        db.execute("INSERT INTO marks(id,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,dept_id,student_id,year) VALUES(:i,:s1,:s2,:s3,:s4,:s5,:s6,:s7,:s8,:d,:s,:y)", {"i":id,"s1": sub1, "s2": sub2, "s3": sub3, "s4":sub4, "s5":sub5, "s6":sub6, "s7":sub7, "s8":sub8,"d":dept_id, "s":student_id, "y":year})
                    db.commit()
                elif table=="Profile":
                    for sid,name,branch,year,gender,dob,phone,entrance_type,father_name,father_number in reader:
                        db.execute("INSERT INTO student_profile(sid,name,branch,year,gender,dob,phone,entrance_type,father_name,father_number) VALUES(:a, :b, :c,:d,:e,:f,:g,:h,:i,:j)", {"a":sid,"b": name,"c": branch,"d": year,"e": gender,"f": dob,"g": phone,"h": entrance_type,"i": father_name,"j":father_number})
                    db.commit()
                elif table=="Faculty":
                    for id, name, dept_id in reader:
                        db.execute("INSERT INTO faculty(id, name, dept_id) VALUES(:s, :n, :d)", {"s":id, "n":name, "d":dept_id })
                    db.commit()
            except:
                message = "columns must be in correct order {}".format(str_to_class(table).__table__.columns.keys())
                return render_template('load_data.html', output=message)
        except exc.SQLAlchemyError:
            message = "columns must be in correct order {}".format(str_to_class(table).__table__.columns.keys())
            return render_template('load_data.html', output=message)
    return render_template("load_data.html")
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
            result = db.execute("INSERT INTO accounts (id,name,user_type,password) VALUES (:u,:n,:t,:p)", {"u": usern,"n":name,"t":usert ,"p": passw_hash})
            db.commit()
            if result.rowcount > 0:
                session['user'] = usern
                session['namet'] = name
                session['usert'] = usert
                flash("Your successfully Registrated")
                return redirect(url_for('dashboard'))
        except exc.IntegrityError:
            message = "Roll Number already exists."
            db.execute("ROLLBACK")
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
            exist=db.execute("SELECT password FROM accounts WHERE id = :u", {"u": session['user']}).fetchone()
            if bcrypt.check_password_hash(exist['password'], epswd) is True:
                res=db.execute("UPDATE accounts SET password = :u WHERE id = :v",{"u":passw_hash,"v":session['user']})
                db.commit()
                if res.rowcount > 0:
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
            res=db.execute("UPDATE accounts SET password = :u WHERE id = :v",{"u":passw_hash,"v":rollno})
            db.commit()
            if res is not None:
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
        result = db.execute("SELECT * FROM accounts WHERE id = :u", {"u": usern}).fetchone()

        if result is not None:
            print(result['password'])
            if bcrypt.check_password_hash(result['password'], passw) is True:
                session['user'] = usern
                session['namet'] = result.name
                session['usert'] = result.user_type
                flash("Hii  "+result.name)
                return redirect(url_for('dashboard'))

        message = "Username or password is incorrect."
    return render_template("login.html", message=message)

# Main
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port=5000)