from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Employee(db.Model):
    """Employee model for storing employee information"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(80), nullable=False, index=True)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    joining_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active')  # Active, Inactive, On Leave
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='employee', lazy=True, cascade='all, delete-orphan')
    salary_records = db.relationship('SalaryRecord', backref='employee', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Employee {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'position': self.position,
            'salary': self.salary,
            'joining_date': self.joining_date.strftime('%Y-%m-%d') if self.joining_date else None,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class Attendance(db.Model):
    """Attendance tracking model"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), default='Present')  # Present, Absent, Late, Sick Leave, Casual Leave
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='_employee_date_uc'),)
    
    def __repr__(self):
        return f'<Attendance {self.employee_id} - {self.date}>'


class SalaryRecord(db.Model):
    """Salary and payroll management model"""
    __tablename__ = 'salary_records'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, index=True)
    month = db.Column(db.String(7), nullable=False)  # Format: YYYY-MM
    basic_salary = db.Column(db.Float, nullable=False)
    allowances = db.Column(db.Float, default=0)  # DA, HRA, etc
    deductions = db.Column(db.Float, default=0)  # Tax, Insurance, etc
    net_salary = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='Pending')  # Pending, Paid, Failed
    payment_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'month', name='_employee_month_uc'),)
    
    def __repr__(self):
        return f'<SalaryRecord {self.employee_id} - {self.month}>'
