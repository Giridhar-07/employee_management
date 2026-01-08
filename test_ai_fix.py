#!/usr/bin/env python
"""Test script to verify AI endpoints are working after fix."""

import requests
import json
import sys
from requests.sessions import Session

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'
AI_ENDPOINT = f'{BASE_URL}/api/ai/salary-recommendation/1'

def test_ai_endpoints():
    """Test AI endpoints with session login."""
    print("=" * 70)
    print("Testing AI Endpoints After Fix")
    print("=" * 70)
    
    session = requests.Session()
    
    # Step 1: Login
    print("\n[STEP 1] Attempting login with admin credentials...")
    login_data = {
        'email': 'admin@example.com',
        'password': 'admin123'
    }
    
    try:
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print("  [OK] Login successful (received 200)")
        else:
            print(f"  [FAIL] Login failed with status {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"  [FAIL] Login error: {str(e)}")
        return False
    
    # Step 2: Test AI salary recommendation endpoint
    print(f"\n[STEP 2] Testing AI salary recommendation endpoint...")
    print(f"  Endpoint: {AI_ENDPOINT}")
    
    try:
        response = session.get(AI_ENDPOINT)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("  [OK] Received 200 status code")
            if 'recommendation' in data:
                recommendation = data['recommendation']
                print(f"  [OK] AI recommendation received ({len(recommendation)} chars)")
                print(f"\n  Sample output:\n  {recommendation[:200]}...")
                return True
            else:
                print(f"  [FAIL] No 'recommendation' key in response")
                print(f"  Response keys: {list(data.keys())}")
                return False
        elif response.status_code == 503:
            print(f"  [FAIL] Received 503 Service Unavailable")
            data = response.json()
            print(f"  Error message: {data.get('error', 'Unknown error')}")
            return False
        else:
            print(f"  [FAIL] Unexpected status code: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
    except requests.exceptions.ConnectionError as e:
        print("  [FAIL] Could not connect to server. Make sure Flask is running on port 5000")
        print(f"  Error: {str(e)}")
        return False
    except Exception as e:
        print(f"  [FAIL] Error: {str(e)}")
        return False


if __name__ == '__main__':
    success = test_ai_endpoints()
    
    print("\n" + "=" * 70)
    if success:
        print("[SUCCESS] All tests PASSED - AI endpoints are working!")
        print("=" * 70)
        sys.exit(0)
    else:
        print("[FAILED] Tests FAILED - See errors above")
        print("=" * 70)
        sys.exit(1)
