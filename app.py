"""
College Automation System - Main Application
Refactored with Flask Blueprints for better code organization
All routes moved to views/ directory
"""

import os
import sys
from flask import Flask, session, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_session import Session
from database import Base
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import matplotlib
from matplotlib import pyplot as plt

# Configure matplotlib
matplotlib.use('Agg')

# ============================================
# FLASK APP INITIALIZATION
# ============================================

app = Flask(__name__)

# Configuration
app.secret_key = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Initialize extensions
bcrypt = Bcrypt(app)
session_manager = Session(app)

# ============================================
# DATABASE SETUP
# ============================================

# Create database engine
engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False}, echo=False)
Base.metadata.bind = engine

# Disable bound value tracking for better performance
def disable_bound_value_tracking(dbapi_con, con_record):
    dbapi_con.execute('PRAGMA track_bound_values = OFF')

event.listen(engine, 'connect', disable_bound_value_tracking)

# Create database session
DBSession = sessionmaker(bind=engine)
db = DBSession()

# Make db available globally for blueprints
app.db = db

# ============================================
# BLUEPRINT REGISTRATION
# ============================================

# Import and initialize all blueprints
from views.dashboard import dashboard_bp
from views.auth import auth_bp, init_auth
from views.student import student_bp, init_student
from views.query import query_bp, init_query
from views.chatbot import chatbot_bp, init_chatbot
from views.feedback import feedback_bp, init_feedback
from views.admin import admin_bp, init_admin
from views.counselor import counselor_bp, init_counselor

# Initialize blueprints with database and extensions
init_auth(bcrypt, db)
init_student(db)
init_query(db)
init_chatbot(db)
init_feedback(db)
init_admin(db)
init_counselor(db)

# Register blueprints with app
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(query_bp, url_prefix='/query')
app.register_blueprint(chatbot_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(counselor_bp)

# ============================================
# MAIN ROUTES
# ============================================

@app.route("/")
def index():
    """Main entry point"""
    if 'user' not in session:
        return render_template("intro.html")
    else:
        return redirect(url_for('dashboard.main'))


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template("error.html", error_code=404, error_msg="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.rollback()
    return render_template("error.html", error_code=500, error_msg="Internal server error"), 500


# ============================================
# CONTEXT PROCESSORS
# ============================================

@app.context_processor
def inject_user():
    """Inject user info into templates"""
    return dict(
        current_user=session.get('user'),
        current_username=session.get('namet'),
        current_user_type=session.get('usert')
    )


# ============================================
# APP STARTUP
# ============================================

if __name__ == '__main__':
    app.debug = False
    app.run(host='127.0.0.1', port=8002, use_reloader=False)
