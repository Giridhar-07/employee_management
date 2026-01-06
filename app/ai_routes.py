"""Add to the end of app/routes.py to add AI-powered endpoints."""

# ======= AI-Powered Insights API =======
from app.ai_service import get_ai_client

@main_bp.route('/api/ai/salary-recommendation/<int:employee_id>')
def api_salary_recommendation(employee_id):
    """Get AI salary recommendation for an employee"""
    employee = Employee.query.get_or_404(employee_id)
    ai = get_ai_client()
    
    if not ai:
        return jsonify({'error': 'AI service not available'}), 503
    
    # Calculate years of experience
    years_exp = None
    if employee.joining_date:
        delta = datetime.now() - employee.joining_date
        years_exp = delta.days / 365.25
    
    recommendation = ai.get_salary_recommendation(
        employee.name,
        employee.position,
        employee.department,
        employee.salary,
        years_exp
    )
    
    return jsonify({'recommendation': recommendation})


@main_bp.route('/api/ai/performance-insight/<int:employee_id>')
def api_performance_insight(employee_id):
    """Get AI performance insight for an employee"""
    employee = Employee.query.get_or_404(employee_id)
    ai = get_ai_client()
    
    if not ai:
        return jsonify({'error': 'AI service not available'}), 503
    
    # Calculate attendance score
    last_30_days = date.today() - timedelta(days=30)
    total_days = Attendance.query.filter(
        and_(
            Attendance.employee_id == employee_id,
            Attendance.date >= last_30_days
        )
    ).count()
    
    present_days = Attendance.query.filter_by(
        employee_id=employee_id,
        status='Present'
    ).filter(Attendance.date >= last_30_days).count()
    
    attendance_score = (present_days / total_days * 100) if total_days > 0 else 0
    
    # Calculate months employed
    months_employed = 0
    if employee.joining_date:
        delta = datetime.now() - employee.joining_date
        months_employed = delta.days // 30
    
    insight = ai.get_performance_insight(
        employee.name,
        employee.department,
        attendance_score,
        months_employed
    )
    
    return jsonify({'insight': insight})


@main_bp.route('/api/ai/attendance-analysis/<int:employee_id>')
def api_attendance_analysis(employee_id):
    """Get AI attendance analysis"""
    employee = Employee.query.get_or_404(employee_id)
    ai = get_ai_client()
    
    if not ai:
        return jsonify({'error': 'AI service not available'}), 503
    
    last_30_days = date.today() - timedelta(days=30)
    total_days = Attendance.query.filter(
        and_(
            Attendance.employee_id == employee_id,
            Attendance.date >= last_30_days
        )
    ).count()
    
    present_days = Attendance.query.filter_by(
        employee_id=employee_id,
        status='Present'
    ).filter(Attendance.date >= last_30_days).count()
    
    absent_days = total_days - present_days
    
    analysis = ai.get_attendance_analysis(
        employee.name,
        present_days,
        absent_days,
        total_days
    )
    
    return jsonify({'analysis': analysis})


@main_bp.route('/api/ai/department-insights/<department>')
def api_department_insights(department):
    """Get AI insights for a department"""
    ai = get_ai_client()
    
    if not ai:
        return jsonify({'error': 'AI service not available'}), 503
    
    employees = Employee.query.filter_by(department=department).all()
    total_employees = len(employees)
    
    if total_employees == 0:
        return jsonify({'insight': 'No employees in this department'})
    
    avg_salary = sum(e.salary for e in employees) / total_employees
    
    # Calculate average attendance
    last_30_days = date.today() - timedelta(days=30)
    all_attendance = Attendance.query.filter(
        Attendance.employee_id.in_([e.id for e in employees]),
        Attendance.date >= last_30_days
    ).all()
    
    present_count = sum(1 for a in all_attendance if a.status == 'Present')
    avg_attendance = (present_count / len(all_attendance) * 100) if all_attendance else 0
    
    insight = ai.get_department_insights(
        department,
        total_employees,
        avg_salary,
        avg_attendance
    )
    
    return jsonify({'insight': insight})
