"""Test AI API endpoints directly."""
import sys
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import Employee
from datetime import date

# Create app in development mode (uses PostgreSQL)
app = create_app('development')

with app.test_client() as client:
    with app.app_context():
        # Check if there are employees
        emp_count = Employee.query.count()
        print(f'Total employees in database: {emp_count}')
        
        if emp_count == 0:
            print('No employees found. Creating test employee...')
            test_emp = Employee(
                name='AI Test Employee',
                email='ai_test@example.com',
                phone='555-1234',
                department='IT',
                position='Developer',
                salary=50000,
                joining_date=date(2024, 1, 1),
                status='Active'
            )
            db.session.add(test_emp)
            db.session.commit()
            emp_id = test_emp.id
            print(f'Created test employee with ID: {emp_id}')
        else:
            emp_id = Employee.query.first().id
            emp = Employee.query.get(emp_id)
            print(f'Using existing employee: {emp.name} (ID: {emp_id})')
        
        # Test AI endpoints
        print('\n=== Testing AI Endpoints ===')
        
        # Test salary recommendation
        print(f'\n1) Testing /api/ai/salary-recommendation/{emp_id}')
        r = client.get(f'/api/ai/salary-recommendation/{emp_id}')
        print(f'   Status: {r.status_code}')
        print(f'   Response: {r.get_json()}')
        
        # Test performance insight
        print(f'\n2) Testing /api/ai/performance-insight/{emp_id}')
        r = client.get(f'/api/ai/performance-insight/{emp_id}')
        print(f'   Status: {r.status_code}')
        print(f'   Response: {r.get_json()}')
        
        # Test attendance analysis
        print(f'\n3) Testing /api/ai/attendance-analysis/{emp_id}')
        r = client.get(f'/api/ai/attendance-analysis/{emp_id}')
        print(f'   Status: {r.status_code}')
        print(f'   Response: {r.get_json()}')
        
        # Test department insights
        print(f'\n4) Testing /api/ai/department-insights/IT')
        r = client.get(f'/api/ai/department-insights/IT')
        print(f'   Status: {r.status_code}')
        print(f'   Response: {r.get_json()}')
        
        print('\n=== All AI Endpoint Tests Complete ===')
