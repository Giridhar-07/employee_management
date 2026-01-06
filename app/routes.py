from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, date, timedelta
from app.models import db, Employee, Attendance, SalaryRecord
from sqlalchemy import and_, or_, func
import csv
from io import StringIO

# Define blueprints
main_bp = Blueprint('main', __name__)
employee_bp = Blueprint('employees', __name__)
attendance_bp = Blueprint('attendance', __name__)
salary_bp = Blueprint('salary', __name__)


# ==================== MAIN ROUTES ====================
@main_bp.route('/')
def index():
    """Dashboard with statistics"""
    total_employees = Employee.query.count()
    active_employees = Employee.query.filter_by(status='Active').count()
    departments = db.session.query(Employee.department, func.count(Employee.id)).group_by(Employee.department).all()
    
    # Today's attendance
    today = date.today()
    today_attendance = Attendance.query.filter_by(date=today).count()
    
    stats = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'departments': len(departments),
        'today_attendance': today_attendance
    }
    
    return render_template('dashboard.html', stats=stats, departments=departments)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


# ==================== EMPLOYEE ROUTES ====================
@employee_bp.route('/')
def list_employees():
    """List all employees with search and filter"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = Employee.query
    
    # Search functionality
    search = request.args.get('search', '')
    if search:
        query = query.filter(
            or_(
                Employee.name.ilike(f'%{search}%'),
                Employee.email.ilike(f'%{search}%'),
                Employee.position.ilike(f'%{search}%')
            )
        )
    
    # Filter by department
    department = request.args.get('department', '')
    if department:
        query = query.filter_by(department=department)
    
    # Filter by status
    status = request.args.get('status', '')
    if status:
        query = query.filter_by(status=status)
    
    # Sort
    sort_by = request.args.get('sort_by', 'name')
    if sort_by == 'salary':
        query = query.order_by(Employee.salary.desc())
    elif sort_by == 'department':
        query = query.order_by(Employee.department)
    else:
        query = query.order_by(Employee.name)
    
    employees = query.paginate(page=page, per_page=per_page)
    
    # Get unique departments for filter dropdown
    departments = db.session.query(Employee.department).distinct().all()
    departments = [d[0] for d in departments]
    
    return render_template('employees/list.html', 
                         employees=employees, 
                         search=search, 
                         department=department,
                         status=status,
                         departments=departments)


@employee_bp.route('/add', methods=['GET', 'POST'])
def add_employee():
    """Add new employee"""
    if request.method == 'POST':
        try:
            # Validate email uniqueness
            if Employee.query.filter_by(email=request.form.get('email')).first():
                flash('Email already exists!', 'danger')
                return redirect(url_for('employees.add_employee'))
            
            employee = Employee(
                name=request.form.get('name').strip(),
                email=request.form.get('email').strip(),
                phone=request.form.get('phone').strip(),
                department=request.form.get('department').strip(),
                position=request.form.get('position').strip(),
                salary=float(request.form.get('salary')),
                joining_date=datetime.strptime(request.form.get('joining_date'), '%Y-%m-%d'),
                status='Active'
            )
            
            db.session.add(employee)
            db.session.commit()
            flash(f'Employee {employee.name} added successfully!', 'success')
            return redirect(url_for('employees.list_employees'))
        
        except ValueError as e:
            flash('Invalid input data. Please check your entries.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('employees/add.html')


@employee_bp.route('/<int:employee_id>')
def view_employee(employee_id):
    """View employee details"""
    employee = Employee.query.get_or_404(employee_id)
    
    # Get attendance for last 30 days
    last_30_days = date.today() - timedelta(days=30)
    recent_attendance = Attendance.query.filter(
        and_(
            Attendance.employee_id == employee_id,
            Attendance.date >= last_30_days
        )
    ).order_by(Attendance.date.desc()).all()
    
    # Get current month salary record
    current_month = datetime.now().strftime('%Y-%m')
    salary_record = SalaryRecord.query.filter_by(
        employee_id=employee_id,
        month=current_month
    ).first()
    
    # Calculate attendance stats
    present_count = Attendance.query.filter_by(
        employee_id=employee_id,
        status='Present'
    ).filter(Attendance.date >= last_30_days).count()
    
    absent_count = Attendance.query.filter_by(
        employee_id=employee_id,
        status='Absent'
    ).filter(Attendance.date >= last_30_days).count()
    
    return render_template('employees/view.html', 
                         employee=employee,
                         recent_attendance=recent_attendance,
                         salary_record=salary_record,
                         present_count=present_count,
                         absent_count=absent_count)


@employee_bp.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Edit employee"""
    employee = Employee.query.get_or_404(employee_id)
    
    if request.method == 'POST':
        try:
            # Check if new email is unique (excluding current employee)
            new_email = request.form.get('email').strip()
            if new_email != employee.email:
                if Employee.query.filter_by(email=new_email).first():
                    flash('Email already exists!', 'danger')
                    return redirect(url_for('employees.edit_employee', employee_id=employee_id))
                employee.email = new_email
            
            employee.name = request.form.get('name').strip()
            employee.phone = request.form.get('phone').strip()
            employee.department = request.form.get('department').strip()
            employee.position = request.form.get('position').strip()
            employee.salary = float(request.form.get('salary'))
            employee.status = request.form.get('status')
            employee.joining_date = datetime.strptime(request.form.get('joining_date'), '%Y-%m-%d')
            
            db.session.commit()
            flash(f'Employee {employee.name} updated successfully!', 'success')
            return redirect(url_for('employees.view_employee', employee_id=employee_id))
        
        except ValueError:
            flash('Invalid input data.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('employees/edit.html', employee=employee)


@employee_bp.route('/<int:employee_id>/delete', methods=['POST'])
def delete_employee(employee_id):
    """Delete employee"""
    employee = Employee.query.get_or_404(employee_id)
    name = employee.name
    
    try:
        db.session.delete(employee)
        db.session.commit()
        flash(f'Employee {name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting employee: {str(e)}', 'danger')
    
    return redirect(url_for('employees.list_employees'))


@employee_bp.route('/export/csv')
def export_csv():
    """Export employees to CSV"""
    from flask import make_response
    
    employees = Employee.query.all()
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Email', 'Phone', 'Department', 'Position', 'Salary', 'Joining Date', 'Status'])
    
    for emp in employees:
        cw.writerow([
            emp.id,
            emp.name,
            emp.email,
            emp.phone,
            emp.department,
            emp.position,
            emp.salary,
            emp.joining_date.strftime('%Y-%m-%d') if emp.joining_date else '',
            emp.status
        ])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=employees.csv"
    output.headers["Content-type"] = "text/csv"
    return output


# ======= Simple JSON API for real-time UI updates =======
@main_bp.route('/api/employees')
def api_employees():
    """Return a JSON list of recent employees"""
    employees = Employee.query.order_by(Employee.id.desc()).limit(100).all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'email': e.email,
        'department': e.department,
        'position': e.position,
        'status': e.status
    } for e in employees])


@main_bp.route('/api/stats')
def api_stats():
    """Return simple statistics used by the dashboard"""
    total = Employee.query.count()
    active = Employee.query.filter_by(status='Active').count()
    departments = db.session.query(Employee.department, db.func.count(Employee.id)).group_by(Employee.department).all()
    today = date.today()
    today_att = Attendance.query.filter(Attendance.date == today, Attendance.status == 'Present').count()
    return jsonify({
        'total_employees': total,
        'active_employees': active,
        'departments': len(departments),
        'today_attendance': today_att
    })


# ==================== ATTENDANCE ROUTES ====================
@attendance_bp.route('/')
def attendance_list():
    """View attendance records"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = Attendance.query
    
    # Filter by employee
    employee_id = request.args.get('employee_id', '')
    if employee_id:
        query = query.filter_by(employee_id=int(employee_id))
    
    # Filter by date range
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')
    
    if from_date:
        query = query.filter(Attendance.date >= datetime.strptime(from_date, '%Y-%m-%d').date())
    
    if to_date:
        query = query.filter(Attendance.date <= datetime.strptime(to_date, '%Y-%m-%d').date())
    
    # Filter by status
    status = request.args.get('status', '')
    if status:
        query = query.filter_by(status=status)
    
    attendance_records = query.order_by(Attendance.date.desc()).paginate(page=page, per_page=per_page)
    employees = Employee.query.all()
    
    return render_template('attendance/list.html',
                         attendance_records=attendance_records,
                         employees=employees,
                         employee_id=employee_id,
                         from_date=from_date,
                         to_date=to_date,
                         status=status)


@attendance_bp.route('/mark', methods=['GET', 'POST'])
def mark_attendance():
    """Mark attendance for employees"""
    if request.method == 'POST':
        try:
            employee_id = request.form.get('employee_id')
            date_str = request.form.get('date')
            status = request.form.get('status')
            notes = request.form.get('notes', '')
            
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Check if record exists
            existing = Attendance.query.filter_by(
                employee_id=int(employee_id),
                date=date_obj
            ).first()
            
            if existing:
                existing.status = status
                existing.notes = notes
                message = 'Attendance updated successfully!'
            else:
                attendance = Attendance(
                    employee_id=int(employee_id),
                    date=date_obj,
                    status=status,
                    notes=notes
                )
                db.session.add(attendance)
                message = 'Attendance marked successfully!'
            
            db.session.commit()
            flash(message, 'success')
            return redirect(url_for('attendance.attendance_list'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    employees = Employee.query.filter_by(status='Active').all()
    return render_template('attendance/mark.html', employees=employees)


@attendance_bp.route('/bulk-mark', methods=['GET', 'POST'])
def bulk_mark_attendance():
    """Mark attendance for multiple employees at once"""
    if request.method == 'POST':
        try:
            date_str = request.form.get('date')
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            employees = Employee.query.filter_by(status='Active').all()
            success_count = 0
            
            for emp in employees:
                status = request.form.get(f'status_{emp.id}', 'Present')
                notes = request.form.get(f'notes_{emp.id}', '')
                
                existing = Attendance.query.filter_by(
                    employee_id=emp.id,
                    date=date_obj
                ).first()
                
                if existing:
                    existing.status = status
                    existing.notes = notes
                else:
                    attendance = Attendance(
                        employee_id=emp.id,
                        date=date_obj,
                        status=status,
                        notes=notes
                    )
                    db.session.add(attendance)
                
                success_count += 1
            
            db.session.commit()
            flash(f'Attendance marked for {success_count} employees!', 'success')
            return redirect(url_for('attendance.attendance_list'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    employees = Employee.query.filter_by(status='Active').all()
    return render_template('attendance/bulk_mark.html', employees=employees)


# ==================== SALARY ROUTES ====================
@salary_bp.route('/')
def salary_list():
    """View salary records"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = SalaryRecord.query
    
    # Filter by employee
    employee_id = request.args.get('employee_id', '')
    if employee_id:
        query = query.filter_by(employee_id=int(employee_id))
    
    # Filter by month
    month = request.args.get('month', '')
    if month:
        query = query.filter_by(month=month)
    
    # Filter by status
    status = request.args.get('status', '')
    if status:
        query = query.filter_by(payment_status=status)
    
    salary_records = query.order_by(SalaryRecord.month.desc()).paginate(page=page, per_page=per_page)
    employees = Employee.query.all()
    
    return render_template('salary/list.html',
                         salary_records=salary_records,
                         employees=employees,
                         employee_id=employee_id,
                         month=month,
                         status=status)


@salary_bp.route('/generate', methods=['GET', 'POST'])
def generate_salary():
    """Generate salary for a month"""
    if request.method == 'POST':
        try:
            month = request.form.get('month')
            
            # Check if salary already exists for this month
            existing = SalaryRecord.query.filter_by(month=month).first()
            if existing:
                flash('Salary already generated for this month!', 'warning')
                return redirect(url_for('salary.generate_salary'))
            
            employees = Employee.query.filter_by(status='Active').all()
            success_count = 0
            
            for emp in employees:
                allowances = float(request.form.get(f'allowances_{emp.id}', 0))
                deductions = float(request.form.get(f'deductions_{emp.id}', 0))
                
                net_salary = emp.salary + allowances - deductions
                
                salary_record = SalaryRecord(
                    employee_id=emp.id,
                    month=month,
                    basic_salary=emp.salary,
                    allowances=allowances,
                    deductions=deductions,
                    net_salary=net_salary,
                    payment_status='Pending'
                )
                db.session.add(salary_record)
                success_count += 1
            
            db.session.commit()
            flash(f'Salary generated for {success_count} employees!', 'success')
            return redirect(url_for('salary.salary_list'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    employees = Employee.query.filter_by(status='Active').all()
    current_month = datetime.now().strftime('%Y-%m')
    
    return render_template('salary/generate.html', employees=employees, current_month=current_month)


@salary_bp.route('/<int:salary_id>/mark-paid', methods=['POST'])
def mark_salary_paid(salary_id):
    """Mark salary as paid"""
    salary = SalaryRecord.query.get_or_404(salary_id)
    
    try:
        salary.payment_status = 'Paid'
        salary.payment_date = datetime.utcnow()
        db.session.commit()
        flash('Salary marked as paid!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('salary.salary_list'))
