"""End-to-end functional test for employee flows using requests against running server."""
import requests
from datetime import date

BASE = 'http://127.0.0.1:5000'

session = requests.Session()

print('1) GET /employees/ (list)')
r = session.get(f'{BASE}/employees/')
print(' status', r.status_code)
assert r.status_code == 200, '/employees list failed'

# Create a new employee
print('\n2) POST /employees/add (create)')
payload = {
    'name': 'E2E User',
    'email': f'e2e_user_{int(date.today().strftime("%d"))}@example.com',
    'phone': '555-0101',
    'department': 'QA',
    'position': 'Tester',
    'salary': '3500.00',
    'joining_date': date.today().isoformat()
}
# Follow redirects to final page
r = session.post(f'{BASE}/employees/add', data=payload, allow_redirects=True)
print(' status', r.status_code)
assert r.status_code in (200, 302), 'create failed'

# Find created employee by listing
print('\n3) Verify new employee appears in list')
r = session.get(f'{BASE}/employees/')
assert r.status_code == 200
body = r.text
assert 'E2E User' in body, 'Created employee not in list'
print(' Found E2E User in employees list')

# Get the employee ID by searching the employees page for link to /employees/<id>
import re
m = re.search(r"/employees/(\d+)">\s*E2E User", body)
if m:
    emp_id = int(m.group(1))
else:
    # fallback: search link with E2E User near it
    m = re.search(r"<a href=\"/employees/(\d+)/\">\s*View", body)
    emp_id = int(m.group(1)) if m else None

print(' employee id detected:', emp_id)
assert emp_id, 'Could not detect employee id'

# View employee page
print('\n4) GET /employees/<id> (view)')
r = session.get(f'{BASE}/employees/{emp_id}')
print(' status', r.status_code)
assert r.status_code == 200
assert 'E2E User' in r.text
print(' Employee view OK')

# Edit employee
print('\n5) POST /employees/<id>/edit (update)')
edit_payload = {
    'name': 'E2E User Edited',
    'email': payload['email'],
    'phone': payload['phone'],
    'department': payload['department'],
    'position': payload['position'],
    'salary': payload['salary'],
    'joining_date': payload['joining_date'],
    'status': 'Active'
}
r = session.post(f'{BASE}/employees/{emp_id}/edit', data=edit_payload, allow_redirects=True)
print(' status', r.status_code)
assert r.status_code in (200,302)

# Confirm change
r = session.get(f'{BASE}/employees/{emp_id}')
assert 'E2E User Edited' in r.text
print(' Edit confirmed')

# Delete employee
print('\n6) POST /employees/<id>/delete (delete)')
r = session.post(f'{BASE}/employees/{emp_id}/delete', allow_redirects=True)
print(' status', r.status_code)
assert r.status_code in (200,302)

# Confirm deletion by listing
r = session.get(f'{BASE}/employees/')
assert 'E2E User Edited' not in r.text
print(' Deletion confirmed')

print('\nALL E2E TESTS PASSED')
