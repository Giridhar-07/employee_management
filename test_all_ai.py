"""Comprehensive test of all AI endpoints."""
import requests
import json

session = requests.Session()

# Login
print("Logging in...")
r = session.post('http://127.0.0.1:5000/auth/login', data={
    'email': 'admin@example.com',
    'password': 'admin123'
})
print(f"Login status: {r.status_code}")

endpoints = [
    ('Salary Recommendation', '/api/ai/salary-recommendation/1'),
    ('Performance Insight', '/api/ai/performance-insight/1'),
    ('Attendance Analysis', '/api/ai/attendance-analysis/1'),
]

print("\nTesting AI Endpoints:")
print("=" * 70)

for name, endpoint in endpoints:
    r = session.get(f'http://127.0.0.1:5000{endpoint}')
    status = "PASS" if r.status_code == 200 else "FAIL"
    try:
        data = r.json()
        keys = list(data.keys())
        print(f"[{status}] {name}")
        print(f"  Status: {r.status_code}")
        print(f"  Response keys: {keys}")
        for key in keys:
            if key != 'error':
                content = data[key]
                preview = content[:80] + "..." if len(content) > 80 else content
                print(f"  {key}: {preview}")
        print()
    except Exception as e:
        print(f"[FAIL] {name}")
        print(f"  Status: {r.status_code}")
        print(f"  Error: {str(e)}")
        print(f"  Response: {r.text[:100]}")
        print()
