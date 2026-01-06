import os
# Load environment variables early so config picks up DATABASE_URL
from dotenv import load_dotenv
load_dotenv()
from app import create_app, db
from flask import redirect

app = create_app()

# Security Headers Middleware
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # Updated CSP to allow jQuery, Bootstrap, and Google Fonts
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://code.jquery.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https:; "
        "frame-ancestors 'self'"
    )
    response.headers['Content-Security-Policy'] = csp
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# SSL Redirect in Production
@app.before_request
def before_request():
    """Redirect to HTTPS in production"""
    if os.environ.get('FLASK_ENV') == 'production':
        from flask import request
        if request.headers.get('X-Forwarded-Proto', 'http') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

@app.shell_context_processor
def make_shell_context():
    """Create shell context for Flask CLI"""
    from app.models import Employee, Attendance, SalaryRecord
    return {'db': db, 'Employee': Employee, 'Attendance': Attendance, 'SalaryRecord': SalaryRecord}

if __name__ == '__main__':
    # In production, use: gunicorn wsgi:app --bind 0.0.0.0:5000
    app.run(debug=False, host='0.0.0.0', port=5000)

