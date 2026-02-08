"""
Dashboard and main application routes blueprint
"""

from flask import Blueprint, render_template, session, redirect, url_for

# Initialize blueprint
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/")
def index():
    """
    Home page / root route
    Shows intro page for anonymous users, redirects authenticated users to dashboard
    """
    if 'user' not in session:
        return render_template("intro.html")
    else:
        return redirect(url_for('dashboard.main'))


@dashboard_bp.route("/dashboard")
def main():
    """
    Main dashboard
    Shows appropriate menu based on user type (clerk, admin, student, etc.)
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    user_type = session.get('usert', 'Student')
    
    # Route to appropriate menu based on user type
    if user_type == "clerk":
        return render_template("clerk_menu.html")
    else:
        return render_template("menu.html")


@dashboard_bp.route("/help")
def help():
    """
    Help/documentation page
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template("help.html")
