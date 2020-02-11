import os
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_session import Session
from database import Base, Attendance, Marks,Accounts, Profile, Feedback
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import re
import matplotlib.pyplot as plt
from playsound import playsound
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
    if request.method == 'POST':
        ss=request.form.get("msg")
    if session['usert']=="Student":
        if "show my attendance" in ss:
            return redirect(url_for('attendance'))
        else:
            flash("Wrong! Try Again")
            return redirect(url_for('dashboard'))
    else:
        if "show graph" in ss:
            return redirect(url_for('plot_graph'))
        if "less than 75" in ss:
            result=db.execute("SELECT * FROM attendance WHERE attend < 75 ORDER BY sid").fetchall()
            return render_template("quer.html", results=result)
        elif "65" in ss or "detain" in ss:
            result=db.execute("SELECT * FROM attendance WHERE attend < 65 ORDER BY sid").fetchall()
            return render_template("quer.html", results=result)
        else:
            flash("Wrong! Try Again")
            return redirect(url_for('dashboard'))
    

@app.route("/profile")
def profile():
    res=db.execute("SELECT * FROM student_profile WHERE sid = :u", {"u": session['user']}).fetchall()
    return render_template("profile.html",results=res)

@app.route("/attendance")
def attendance():
    result=db.execute("SELECT * FROM attendance WHERE sid = :u", {"u": session['user']}).fetchall()
    return render_template("attendance.html",results=result)

@app.route("/marks")
def marks():
    return render_template("marks.html")

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
# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    message = ""

    if request.method == "POST":
        try: 
            usern = request.form.get("username")
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
        except exc.IntegrityError:
            message = "Roll Number already exists."
            db.execute("ROLLBACK")
            db.commit()
    return render_template("registration.html", message=message)
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
        usern = request.form.get("username")
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
    app.run(host='0.0.0.0', port=5000)
