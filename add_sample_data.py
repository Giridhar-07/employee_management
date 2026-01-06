#!/usr/bin/env python
"""Insert a test employee into the database to verify NeonDB persistence"""
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import Employee

app = create_app('development')

with app.app_context():
    # create a sample employee
    emp = Employee(name='Test User', email='testuser@example.com', phone='1234567890', department='IT', position='Developer', salary=5000.0)
    db.session.add(emp)
    db.session.commit()
    print(f"Inserted employee id={emp.id} name={emp.name}")
    # verify
    count = db.session.query(Employee).filter_by(email='testuser@example.com').count()
    print(f"Verified records with that email: {count}")
