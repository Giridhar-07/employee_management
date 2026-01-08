from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from functools import wraps
from datetime import datetime, date, timedelta
from app.models import db, Employee, Attendance, SalaryRecord
from app.config import config
import os
import logging

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Configure logging
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        app.logger.setLevel(logging.INFO)
    
    # Register blueprints
    from app.routes import main_bp, employee_bp, attendance_bp, salary_bp
    from app.auth import auth_bp
    
    # Auth blueprint first (so login is accessible without auth)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Other blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(employee_bp, url_prefix='/employees')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(salary_bp, url_prefix='/salary')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
