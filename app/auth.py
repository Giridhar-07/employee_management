"""Authentication module for admin login and session management."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from datetime import datetime
from app.models import db, Admin

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login route"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validate input
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Query admin by email
        admin = Admin.query.filter_by(email=email).first()
        
        if admin and admin.check_password(password) and admin.is_active:
            # Update last login
            admin.last_login = datetime.utcnow()
            db.session.commit()
            
            # Create session
            session['admin_id'] = admin.id
            session['admin_email'] = admin.email
            session['admin_username'] = admin.username
            
            flash(f'Welcome, {admin.full_name or admin.username}!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Admin logout route"""
    admin_username = session.get('admin_username', 'Admin')
    session.clear()
    flash(f'{admin_username} logged out successfully.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.before_app_request
def check_logged_in():
    """Check if admin is logged in and set g.admin"""
    from flask import g
    admin_id = session.get('admin_id')
    g.admin = None
    if admin_id:
        g.admin = Admin.query.get(admin_id)
