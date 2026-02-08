"""
Counselor routes blueprint
Handles: Counselor/Faculty specific operations
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash
from database import Student_Profile
from sqlalchemy import text

# Initialize blueprint
counselor_bp = Blueprint('counselor', __name__)

# Database will be set by app factory
db = None


def init_counselor(db_instance):
    """Initialize counselor blueprint with database"""
    global db
    db = db_instance


@counselor_bp.route("/<sid>/council-students")
def council_students(sid):
    """
    View counsel students for a counselor
    Shows students assigned to the counselor
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    user_type = session.get('usert', 'Student').lower()
    
    # Only counselor can access their counsel students
    if user_type != 'counselor':
        flash("Access denied. This page is for counselors only.", "error")
        return redirect(url_for('dashboard.main'))
    
    try:
        # Get students counseled by this counselor
        counselor_id = session.get('user')
        results = db.query(Student_Profile).filter_by(council_id=counselor_id).all()
        
        if not results:
            flash("No students assigned to you.", "info")
        
        return render_template("counsel_students.html", results=results)
    
    except Exception as e:
        flash(f"Error retrieving counsel students: {str(e)}", "error")
        return redirect(url_for('dashboard.main'))
