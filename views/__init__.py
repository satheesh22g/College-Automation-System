"""
Blueprint initialization and registration
"""

from flask import Blueprint


def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    
    # Import blueprint modules
    from views.auth import auth_bp
    from views.query import query_bp
    from views.admin import admin_bp
    from views.feedback import feedback_bp
    from views.dashboard import dashboard_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(dashboard_bp)


__all__ = ['register_blueprints']
