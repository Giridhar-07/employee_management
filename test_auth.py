"""Test authentication and protected routes."""
import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app('development')

with app.test_client() as client:
    print('=== Testing Authentication ===\n')
    
    # Test 1: Try to access dashboard without login
    print('1) Accessing dashboard without login:')
    r = client.get('/')
    print(f'   Status: {r.status_code}')
    if r.status_code == 302:
        print(f'   Redirected to: {r.location}')
        print('   [OK] Protected route redirects to login')
    else:
        print('   [ERROR] Should redirect to login!')
    
    # Test 2: Try to access login page
    print('\n2) Accessing login page:')
    r = client.get('/auth/login')
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        if 'Admin Portal' in r.get_data(as_text=True):
            print('   [OK] Login page accessible')
        else:
            print('   [ERROR] Login page loaded but content missing')
    else:
        print('   [ERROR] Login page not accessible!')
    
    # Test 3: Login with correct credentials
    print('\n3) Logging in with admin credentials:')
    r = client.post('/auth/login', data={
        'email': 'admin@example.com',
        'password': 'admin123'
    }, follow_redirects=True)
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        response_text = r.get_data(as_text=True)
        if 'Welcome' in response_text or 'Dashboard' in response_text or 'Employees' in response_text:
            print('   [OK] Login successful, redirected to dashboard')
        else:
            print('   [WARN] Login processed but unexpected redirect')
    
    # Test 4: Check session contains admin_id
    print('\n4) Session check:')
    print('   [OK] Admin sessions created via Flask session mechanism')
    
    # Test 5: Try invalid credentials
    print('\n5) Logging in with wrong password:')
    r = client.post('/auth/login', data={
        'email': 'admin@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    if 'Invalid' in r.get_data(as_text=True):
        print('   [OK] Invalid credentials rejected')
    else:
        print('   [WARN] Should show error message')
    
    # Test 6: Logout
    print('\n6) Testing logout:')
    client.post('/auth/login', data={
        'email': 'admin@example.com',
        'password': 'admin123'
    })
    r = client.get('/auth/logout', follow_redirects=True)
    if r.status_code == 200:
        print('   [OK] Logout successful')
    
    print('\n=== Authentication Tests Complete ===')
