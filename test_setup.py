#!/usr/bin/env python
"""Test script to verify NeonDB setup and initialize database"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("COMPANY MANAGEMENT SYSTEM - SETUP VERIFICATION")
print("=" * 60)

try:
    # Initialize Flask app
    print("\n✓ Step 1: Initializing Flask application...")
    from app import create_app, db
    from app.models import Employee, Attendance, SalaryRecord
    
    app = create_app('development')
    print("  ✓ Flask app created successfully")
    
    # Test database connection
    print("\n✓ Step 2: Testing NeonDB connection...")
    with app.app_context():
        # Test connection
        db.session.execute(db.text('SELECT 1'))
        print("  ✓ NeonDB connection successful!")
        
        # Create all tables
        print("\n✓ Step 3: Creating database tables...")
        db.create_all()
        print("  ✓ Tables created/verified")
        
        # Verify tables
        print("\n✓ Step 4: Verifying tables in database...")
        result = db.session.execute(db.text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        ))
        tables = sorted([row[0] for row in result])
        
        for table in tables:
            print(f"  ✓ Table: {table}")
        
        # Check row counts
        print("\n✓ Step 5: Checking table contents...")
        emp_count = db.session.query(Employee).count()
        att_count = db.session.query(Attendance).count()
        sal_count = db.session.query(SalaryRecord).count()
        
        print(f"  • Employees: {emp_count} records")
        print(f"  • Attendance: {att_count} records")
        print(f"  • Salary Records: {sal_count} records")
    
    print("\n" + "=" * 60)
    print("✓✓✓ ALL SETUP VERIFIED SUCCESSFULLY! ✓✓✓")
    print("=" * 60)
    print("\nYou can now run: python wsgi.py")
    print("Or access the app at: http://127.0.0.1:5000")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
