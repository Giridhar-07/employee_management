"""Direct test of AI endpoint using requests library."""
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

# Test AI endpoint
print("\nTesting AI endpoint...")
r = session.get('http://127.0.0.1:5000/api/ai/salary-recommendation/1')
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:500]}")
