"""Create a test admin user for the system."""
import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import Admin

app = create_app('development')

with app.app_context():
    # Check if admin already exists
    admin = Admin.query.filter_by(email='admin@example.com').first()
    
    if admin:
        print('Admin already exists!')
        print(f'Email: {admin.email}')
        print(f'Username: {admin.username}')
    else:
        # Create new admin
        admin = Admin(
            email='admin@example.com',
            username='admin',
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')  # Default password (change this!)
        
        db.session.add(admin)
        db.session.commit()
        
        print('[SUCCESS] Admin user created!')
        print(f'Email: {admin.email}')
        print(f'Username: {admin.username}')
        print(f'Password: admin123')
        print('')
        print('IMPORTANT: Change the password after first login!')
