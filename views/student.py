"""
Student routes blueprint
Handles: Profile, Attendance, Marks display for students
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash
from database import Student_Profile, Attendance, Marks

# Initialize blueprint
student_bp = Blueprint('student', __name__)

# Database will be set by app factory
db = None


def init_student(db_instance):
    """Initialize student blueprint with database"""
    global db
    db = db_instance


@student_bp.route("/profile")
def profile():
    """Fetch and display user profile"""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        user_id = session.get('user')
        user_role = session.get('usert')
        
        if user_role == "Student":
            # Fetch student profile by sid
            student_profile = db.query(Student_Profile).filter_by(sid=user_id).first()
            
            if not student_profile:
                flash("Profile not yet created. Please contact your administrator.", "warning")
                return redirect(url_for('dashboard.main'))
            
            # Fetch related data
            attendance_data = db.query(Attendance).filter_by(student_id=user_id).all() or []
            marks_data = db.query(Marks).filter_by(student_id=user_id).all() or []
            
            return render_template("student_profile.html", 
                                 results=[student_profile], 
                                 marks=marks_data, 
                                 attend=attendance_data)
        else:
            # Faculty/HOD/Counselor profile
            flash("This page is for students only.", "warning")
            return redirect(url_for('dashboard.main'))
    
    except Exception as e:
        flash(f"Error retrieving profile: {str(e)}", "error")
        return redirect(url_for('dashboard.main'))


@student_bp.route("/attendance")
def attendance():
    """Fetch and display attendance records"""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        user_id = session.get('user')
        result = db.query(Attendance).filter_by(student_id=user_id).all() or []
        
        if not result:
            flash("No attendance records found.", "info")
        
        return render_template("attendance.html", results=result)
    except Exception as e:
        flash(f"Error retrieving attendance: {str(e)}", "error")
        return redirect(url_for('dashboard.main'))


@student_bp.route("/marks")
def marks():
    """Fetch and display marks records"""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        user_id = session.get('user')
        result = db.query(Marks).filter_by(student_id=user_id).all() or []
        
        if not result:
            flash("No marks records found.", "info")
        
        return render_template("marks.html", results=result)
    except Exception as e:
        flash(f"Error retrieving marks: {str(e)}", "error")
        return redirect(url_for('dashboard.main'))


@student_bp.route("/attendance_display")
def attendance_display():
    """Attendance form page"""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template("attendance_form.html")
