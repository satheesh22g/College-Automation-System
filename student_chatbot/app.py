import os
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_session import Session

from database import Base, Attendance, Marks,Accounts, Profile
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from nltk.chat.util import Chat, reflections


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(24)
def chatty():
    print("Hi, I'm Chatty and I chat alot ;)\nPlease type lowercase English language to start a conversation. Type quit to leave ") #default message at the start
    chat = Chat(pairs, reflections)
    chat.converse()

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

    return redirect(url_for('dashboard'))
@app.route("/dashboard")
def dashboard():
  
    return render_template("menu.html")


@app.route("/query", methods=["POST"])
def quer():
    message=""
    if request.method == 'POST':
        ss=request.form.get("msg")
    if "less than 75" in ss:
        result=db.execute("SELECT * FROM attendance WHERE attend < 75 ORDER BY sid").fetchall()
        return render_template("quer.html", results=result)
    elif "65" in ss or "detain" in ss:
        result=db.execute("SELECT * FROM attendance WHERE attend < 65 ORDER BY sid").fetchall()
        return render_template("quer.html", results=result)
    else:
        flash("Wrong! Try Again")
        return render_template("menu.html",mess=message)
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/attendance")
def attendance():
    return render_template("attendance.html")
@app.route("/marks")
def marks():
    return render_template("marks.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    message = ""

    if request.method == "POST":
        try: 
            usern = request.form.get("username")
            usert = request.form.get("usertyp")
            passw = request.form.get("password")
            passw_hash = bcrypt.generate_password_hash(passw).decode('utf-8')
            result = db.execute("INSERT INTO accounts (username,user_type,password) VALUES (:u,:t,:p)", {"u": usern,"t":usert ,"p": passw_hash})
            db.commit()

            if result.rowcount > 0:
                session['user'] = usern
               

                
                flash("Your successfully Registrated")
                return redirect(url_for('dashboard'))

        except exc.IntegrityError:
            message = "Roll Number already exists."
            db.execute("ROLLBACK")
            db.commit()
    
    return render_template("registration.html", message=message)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    message = ""

    if request.method == "POST":
        usern = request.form.get("username")
        passw = request.form.get("password").encode('utf-8')
        result = db.execute("SELECT * FROM accounts WHERE username = :u", {"u": usern}).fetchone()

        if result is not None:
            print(result['password'])
            if bcrypt.check_password_hash(result['password'], passw) is True:
                session['user'] = usern
                return redirect(url_for('dashboard'))

        message = "Username or password is incorrect."
    return render_template("login.html", message=message)





if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
