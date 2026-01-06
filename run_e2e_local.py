"""Run full end-to-end functional tests in-process using Flask test client.
This avoids subprocess/shell quoting issues and gives direct tracebacks for root-cause fixes.
"""
import sys
import traceback
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import Employee, Attendance
from datetime import date
import re

import os

# Allow selecting config via env var so CI can run tests in `testing` mode
APP_CONFIG = os.environ.get('APP_CONFIG', 'development')

def find_employee_id_from_list(html, name):
    # Try patterns to find /employees/<id> near the employee name
    # Look for a link with the employee name or an href preceding the name
    m = re.search(rf"/employees/(\d+)[^>]*>\s*{re.escape(name)}", html)
    if m:
        return int(m.group(1))
    # fallback: find all ids and choose one where the name appears within 200 chars
    ids = [m.group(1) for m in re.finditer(r"/employees/(\d+)", html)]
    for id_ in ids:
        # find position of id and check substring
        pos = html.find(f"/employees/{id_}")
        if pos != -1:
            window = html[max(0, pos-200):pos+200]
            if name in window:
                return int(id_)
    return None


def run_tests():
    try:
        app = create_app(APP_CONFIG)
        with app.test_client() as client:
            print('1) GET /employees/ (list)')
            r = client.get('/employees/')
            print(' status', r.status_code)
            assert r.status_code == 200

            # Create employee
            print('\n2) POST /employees/add (create)')
            email = f'e2e_local_{date.today().strftime("%Y%m%d")}_test@example.com'
            payload = {
                'name': 'E2E Local User',
                'email': email,
                'phone': '555-1234',
                'department': 'QA',
                'position': 'Tester',
                'salary': '3200.00',
                'joining_date': date.today().isoformat()
            }
            r = client.post('/employees/add', data=payload, follow_redirects=True)
            print(' status', r.status_code)
            if r.status_code >= 400:
                print('Response body:\n', r.get_data(as_text=True)[:2000])
            assert r.status_code < 400

            # Verify created
            print('\n3) Verify new employee appears in list')
            r = client.get('/employees/')
            body = r.get_data(as_text=True)
            assert 'E2E Local User' in body, 'Created employee name not present in list HTML'
            print(' Found E2E Local User in employees list')

            emp_id = find_employee_id_from_list(body, 'E2E Local User')
            print(' employee id detected:', emp_id)
            assert emp_id is not None, 'Could not detect employee id in list page'

            # View
            print('\n4) GET /employees/<id> (view)')
            r = client.get(f'/employees/{emp_id}')
            print(' status', r.status_code)
            assert r.status_code == 200
            assert 'E2E Local User' in r.get_data(as_text=True)
            print(' Employee view OK')

            # Edit
            print('\n5) POST /employees/<id>/edit (update)')
            edit_payload = payload.copy()
            edit_payload['name'] = 'E2E Local User Edited'
            edit_payload['status'] = 'Active'
            r = client.post(f'/employees/{emp_id}/edit', data=edit_payload, follow_redirects=True)
            print(' status', r.status_code)
            assert r.status_code < 400
            r = client.get(f'/employees/{emp_id}')
            assert 'E2E Local User Edited' in r.get_data(as_text=True)
            print(' Edit confirmed')

            # Delete
            print('\n6) POST /employees/<id>/delete (delete)')
            r = client.post(f'/employees/{emp_id}/delete', follow_redirects=True)
            print(' status', r.status_code)
            assert r.status_code < 400

            r = client.get('/employees/')
            assert 'E2E Local User Edited' not in r.get_data(as_text=True)
            print(' Deletion confirmed')

            print('\nALL IN-PROCESS E2E TESTS PASSED')
    except AssertionError as ae:
        print('\nASSERTION FAILED:', str(ae))
        traceback.print_exc()
        sys.exit(2)
    except Exception as e:
        print('\nERROR during tests:', str(e))
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    run_tests()
