"""
Feedback and suggestions routes blueprint
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database import Feedback, Faculty_Feedback
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exc
from datetime import datetime, timedelta

# Initialize blueprint
feedback_bp = Blueprint('feedback', __name__)

# Will be set by app factory
db = None


def init_feedback(db_instance):
    """Initialize feedback blueprint with database"""
    global db
    db = db_instance


@feedback_bp.route("/suggestions", methods=["GET", "POST"])
def suggestions():
    """
    User feedback and suggestions endpoint
    Auto-captures username from session
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    msg1 = ""
    msg2 = ""
    
    try:
        if request.method == "POST":
            # Get username from session (auto-identification)
            username = session.get('namet', 'Anonymous')
            subject = request.form.get("subject", "").strip()
            message = request.form.get("message", "").strip()
            
            # Validation
            if not all([subject, message]):
                msg1 = "Error"
                msg2 = "Subject and message are required"
            else:
                # Create and store feedback
                new_feedback = Feedback(
                    name=username,
                    subject=subject,
                    message=message,
                    user_id=session['user']
                )
                db.add(new_feedback)
                db.commit()
                
                msg1 = "Submitted!"
                msg2 = "Thank you for your feedback"
                
    except IntegrityError:
        db.rollback()
        msg1 = "Error"
        msg2 = "An error occurred while submitting feedback"
    except Exception as e:
        db.rollback()
        msg1 = "Error"
        msg2 = "An unexpected error occurred"
    
    return render_template("feedback.html", msg1=msg1, msg2=msg2)


@feedback_bp.route("/Faculty-Feedback", methods=["GET", "POST"])
def faculty_feedback():
    """
    Faculty feedback form
    Students rate faculty courses
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    msg1 = ""
    msg2 = ""
    
    try:
        # Clean old feedback (older than 1 day)
        too_old = datetime.today() - timedelta(days=1)
        db.query(Faculty_Feedback).filter(Faculty_Feedback.date <= too_old).delete()
        db.commit()
        
        if request.method == "POST":
            # Get form data
            sub1 = request.form.get("sub1")
            sub2 = request.form.get("sub2")
            sub3 = request.form.get("sub3")
            sub4 = request.form.get("sub4")
            sub5 = request.form.get("sub5")
            sub6 = request.form.get("sub6")
            lab1 = request.form.get("lab1")
            lab2 = request.form.get("lab2")
            
            # Create feedback record
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
            db.add(new_feedback)
            db.commit()
            
            msg1 = "Submitted!"
            msg2 = "Thank you for your feedback"
            
    except IntegrityError:
        db.rollback()
        msg1 = "Already Submitted"
        msg2 = "You have already submitted feedback"
    except Exception as e:
        db.rollback()
        msg1 = "Error"
        msg2 = "An error occurred while submitting feedback"
    
    return render_template("faculty_feedback.html", msg1=msg1, msg2=msg2)


@feedback_bp.route("/feedbacks")
def show_feedback():
    """
    Display faculty feedback to admin/HOD
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        result = db.query(Faculty_Feedback).all()
        return render_template('show_feedback.html', res=result)
    except Exception as e:
        flash("Error retrieving feedbacks", "error")
        return redirect(url_for('dashboard.main'))
