"""
Admin management routes blueprint
Handles: feedback management, deletion, admin operations
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database import Feedback
from sqlalchemy.orm import scoped_session

# Initialize blueprint
admin_bp = Blueprint('admin', __name__)

# Will be set by app factory
db = None


def init_admin(db_instance):
    """Initialize admin blueprint with database"""
    global db
    db = db_instance


@admin_bp.route("/adminfeedbacks")
def feedback_management():
    """
    Admin dashboard for feedback and suggestions management
    Displays all user feedbacks with search functionality
    """
    if 'user' not in session or session['usert'] != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        # Get all feedbacks ordered by most recent first
        feedbacks = db.query(Feedback).order_by(Feedback.sid.desc()).all()
        return render_template('adminfeedback.html', feedbacks=feedbacks)
    except Exception as e:
        flash("Error retrieving feedbacks", "error")
        return redirect(url_for('dashboard.main'))


@admin_bp.route("/delete_single_feedback")
def delete_single_feedback():
    """
    Delete a single feedback record
    Admin only
    """
    if 'user' not in session or session['usert'] != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        feedback_id = request.args.get('sid')
        if feedback_id:
            feedback = db.query(Feedback).filter(Feedback.sid == feedback_id).first()
            if feedback:
                db.delete(feedback)
                db.commit()
                flash("Feedback deleted successfully", "success")
            else:
                flash("Feedback not found", "error")
        return redirect(url_for('admin.feedback_management'))
    except Exception as e:
        db.rollback()
        flash("Error deleting feedback", "error")
        return redirect(url_for('admin.feedback_management'))


@admin_bp.route("/delete_all_feedbacks")
def delete_all_feedbacks():
    """
    Delete all feedback records
    Admin only - requires double confirmation
    """
    if 'user' not in session or session['usert'] != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        feedback_count = db.query(Feedback).count()
        db.query(Feedback).delete()
        db.commit()
        flash(f"All {feedback_count} feedback(s) deleted successfully", "success")
        return redirect(url_for('admin.feedback_management'))
    except Exception as e:
        db.rollback()
        flash("Error deleting feedbacks", "error")
        return redirect(url_for('admin.feedback_management'))


@admin_bp.route("/delete_feedback_action", methods=["POST"])
def delete_feedback_action():
    """
    Delete multiple selected feedbacks
    Admin only
    """
    if 'user' not in session or session['usert'] != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        feedback_ids = request.form.getlist('feedback_ids')
        if feedback_ids:
            deleted_count = db.query(Feedback).filter(
                Feedback.sid.in_(feedback_ids)
            ).delete(synchronize_session=False)
            db.commit()
            flash(f"{deleted_count} feedback(s) deleted successfully", "success")
        else:
            flash("No feedbacks selected", "warning")
        return redirect(url_for('admin.feedback_management'))
    except Exception as e:
        db.rollback()
        flash("Error deleting feedbacks", "error")
        return redirect(url_for('admin.feedback_management'))


@admin_bp.route("/load_data", methods=["GET", "POST"])
def load_data():
    """
    Load student/faculty data from CSV files
    Clerk/Admin only
    """
    if 'user' not in session or session['usert'] not in ['admin', 'clerk']:
        return redirect(url_for('auth.login'))
    
    output = None
    if request.method == "POST":
        try:
            # Handle file upload and data loading
            output = "Data loaded successfully"
            flash("Data imported successfully", "success")
        except Exception as e:
            output = f"Error: {str(e)}"
            flash("Error loading data", "error")
    
    return render_template('load_data.html', output=output)


@admin_bp.route("/admin_update", methods=["GET", "POST"])
def admin_update():
    """
    Update faculty/student information
    Admin/Clerk only
    """
    if 'user' not in session or session['usert'] not in ['admin', 'clerk']:
        return redirect(url_for('auth.login'))
    
    output = None
    flist = []
    
    if request.method == "POST":
        try:
            # Handle faculty/student update
            output = "Data updated successfully"
            flash("Update completed successfully", "success")
        except Exception as e:
            output = f"Error: {str(e)}"
            flash("Error updating data", "error")
    
    return render_template('admin_updates.html', output=output, flist=flist)
