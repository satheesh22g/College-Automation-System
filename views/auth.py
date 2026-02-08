"""
Authentication routes blueprint
Handles: login, register, logout, password change, password reset
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from database import Accounts
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import IntegrityError

# Initialize blueprint
auth_bp = Blueprint('auth', __name__)

# This will be set by the app factory
bcrypt = None
db = None


def init_auth(bcrypt_instance, db_instance):
    """Initialize auth blueprint with bcrypt and database"""
    global bcrypt, db
    bcrypt = bcrypt_instance
    db = db_instance


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    User registration
    Validates input and creates new account
    """
    if 'user' in session:
        return redirect(url_for('dashboard.index'))

    message = ""

    if request.method == "POST":
        try:
            usern = request.form.get("username", "").upper().strip()
            name = request.form.get("name", "").strip()
            usert = request.form.get("usertyp", "").strip()
            passw = request.form.get("password", "").strip()
            
            # Validation
            if not all([usern, name, usert, passw]):
                message = "All fields are required"
            elif len(passw) < 6:
                message = "Password must be at least 6 characters"
            elif len(usern) > 30:
                message = "Username is too long"
            else:
                # Hash password and create account
                passw_hash = bcrypt.generate_password_hash(passw).decode('utf-8')
                new_account = Accounts(id=usern, name=name, user_type=usert, password=passw_hash)
                db.add(new_account)
                db.commit()
                
                # Set session variables
                session['user'] = usern
                session['namet'] = name
                session['usert'] = usert
                
                flash("Successfully registered! Welcome to the system.", 'alert')
                return redirect(url_for('dashboard.index'))
                
        except IntegrityError:
            db.rollback()
            message = "Username already exists. Please choose a different username."
        except Exception as e:
            db.rollback()
            message = "An error occurred during registration. Please try again."
    
    return render_template("registration.html", message=message)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    User login
    Authenticates user credentials and creates session
    """
    if 'user' in session:
        return redirect(url_for('dashboard.index'))
    
    message = ""
    
    if request.method == "POST":
        try:
            usern = request.form.get("username", "").upper().strip()
            passw = request.form.get("password", "").encode('utf-8')
            
            if not usern or not passw:
                message = "Please enter both username and password"
            else:
                # Query database for user
                user = db.query(Accounts).filter_by(id=usern).first()
                
                if user and bcrypt.check_password_hash(user.password, passw):
                    # Create session
                    session['user'] = usern
                    session['namet'] = user.name
                    session['usert'] = user.user_type
                    
                    flash(f"Welcome {user.name}!", "greet")
                    return redirect(url_for('dashboard.index'))
                else:
                    message = "Invalid username or password"
                    
        except Exception as e:
            message = "An error occurred during login. Please try again."
    
    return render_template("login.html", message=message)


@auth_bp.route("/logout")
def logout():
    """
    User logout
    Clears session and redirects to home
    """
    session.pop('user', None)
    session.pop('namet', None)
    session.pop('usert', None)
    flash("You have been logged out successfully", "info")
    return redirect(url_for('index'))


@auth_bp.route("/change-password", methods=["GET", "POST"])
def changepass():
    """
    Change password for logged-in user
    Requires current password and new password confirmation
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    msg = ""
    
    if request.method == "POST":
        try:
            current_pwd = request.form.get("epassword", "").strip()
            new_pwd = request.form.get("cpassword", "").strip()
            confirm_pwd = request.form.get("cpassword_confirm", "").strip()
            
            # Validation
            if not all([current_pwd, new_pwd, confirm_pwd]):
                msg = "All fields are required"
            elif new_pwd != confirm_pwd:
                msg = "New password confirmation does not match"
            elif len(new_pwd) < 6:
                msg = "New password must be at least 6 characters"
            else:
                # Check current password
                user = db.query(Accounts).filter_by(id=session['user']).first()
                
                if user and bcrypt.check_password_hash(user.password, current_pwd.encode('utf-8')):
                    # Update password
                    user.password = bcrypt.generate_password_hash(new_pwd).decode('utf-8')
                    db.commit()
                    
                    flash("Password changed successfully!", "alert")
                    return redirect(url_for('dashboard.index'))
                else:
                    msg = "Current password is incorrect"
                    
        except Exception as e:
            db.rollback()
            msg = "An error occurred while changing password"
    
    return render_template("change_password.html", m=msg)


@auth_bp.route("/reset", methods=["GET", "POST"])
def reset():
    """
    Admin-only password reset
    Resets any user's password to default
    """
    if 'user' not in session or session['usert'] != "admin":
        return redirect(url_for('dashboard.index'))
    
    msg = ""
    
    if request.method == "POST":
        try:
            username = request.form.get("rollno", "").upper().strip()
            
            if not username:
                msg = "Please enter a username"
            else:
                user = db.query(Accounts).filter_by(id=username).first()
                
                if user:
                    # Reset to default password
                    default_password = "defaultpass123"
                    user.password = bcrypt.generate_password_hash(default_password).decode('utf-8')
                    db.commit()
                    
                    flash(f"Password for {username} has been reset to default", "alert")
                    return redirect(url_for('dashboard.index'))
                else:
                    msg = f"User '{username}' not found"
                    
        except Exception as e:
            db.rollback()
            msg = "An error occurred while resetting password"
    
    return render_template("pswdreset.html", m=msg)
