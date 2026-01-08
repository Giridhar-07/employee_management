import requests

BASE = 'http://127.0.0.1:5000'

s = requests.Session()
print('Logging in...')
r = s.post(f'{BASE}/auth/login', data={'email':'admin@example.com','password':'admin123'})
print('Login status', r.status_code)

print('Fetching /analytics')
r = s.get(f'{BASE}/analytics')
print('/analytics', r.status_code)

print('Fetching overview API')
r = s.get(f'{BASE}/api/analytics/overview')
print('/api/analytics/overview', r.status_code)
print('Response:', r.json() if r.status_code==200 else r.text[:200])

print('Done')
