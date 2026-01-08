"""Complete end-to-end test of AI endpoints fix."""
import requests
import time

def test_complete_flow():
    """Test the complete flow: login -> view employee -> access AI endpoints."""
    print("\n" + "="*70)
    print("COMPLETE END-TO-END TEST OF AI ENDPOINTS")
    print("="*70)
    
    session = requests.Session()
    BASE_URL = 'http://127.0.0.1:5000'
    
    # Step 1: Login
    print("\n[STEP 1] Login to Application")
    print("-" * 70)
    r = session.post(f'{BASE_URL}/auth/login', data={
        'email': 'admin@example.com',
        'password': 'admin123'
    })
    print(f"POST /auth/login")
    print(f"Status: {r.status_code} {'[PASS]' if r.status_code == 200 else '[FAIL]'}")
    
    # Step 2: Access home page
    print("\n[STEP 2] Access Home Page")
    print("-" * 70)
    r = session.get(f'{BASE_URL}/')
    print(f"GET /")
    print(f"Status: {r.status_code} {'[PASS]' if r.status_code == 200 else '[FAIL]'}")
    
    # Step 3: View Employee List
    print("\n[STEP 3] View Employee List")
    print("-" * 70)
    r = session.get(f'{BASE_URL}/employees')
    print(f"GET /employees")
    print(f"Status: {r.status_code} {'[PASS]' if r.status_code == 200 else '[FAIL]'}")
    
    # Step 4: View Employee Details
    print("\n[STEP 4] View Employee Details")
    print("-" * 70)
    r = session.get(f'{BASE_URL}/employees/view/1')
    print(f"GET /employees/view/1")
    print(f"Status: {r.status_code} {'[PASS]' if r.status_code == 200 else '[FAIL]'}")
    
    # Step 5: Test All AI Endpoints
    print("\n[STEP 5] Test AI Endpoints")
    print("-" * 70)
    
    ai_tests = [
        ("Salary Recommendation", "/api/ai/salary-recommendation/1"),
        ("Performance Insight", "/api/ai/performance-insight/1"),
        ("Attendance Analysis", "/api/ai/attendance-analysis/1"),
    ]
    
    all_passed = True
    for name, endpoint in ai_tests:
        r = session.get(f'{BASE_URL}{endpoint}')
        passed = r.status_code == 200
        all_passed = all_passed and passed
        status_text = "[PASS]" if passed else "[FAIL]"
        
        print(f"\n  {status_text} {name}")
        print(f"  GET {endpoint}")
        print(f"  Status: {r.status_code}")
        
        if passed:
            data = r.json()
            for key, value in data.items():
                preview = value[:60] + "..." if len(value) > 60 else value
                print(f"  {key}: {preview}")
        else:
            print(f"  Error: {r.text[:100]}")
    
    # Summary
    print("\n" + "="*70)
    if all_passed:
        print("SUCCESS: All tests PASSED - AI endpoints are fully functional!")
        print("="*70)
        return True
    else:
        print("FAILURE: Some tests failed - see details above")
        print("="*70)
        return False

if __name__ == '__main__':
    try:
        success = test_complete_flow()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        exit(1)
