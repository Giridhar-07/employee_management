"""Diagnostic script to identify AI API issues."""
import os
from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("AI ENDPOINT DIAGNOSTIC".center(70))
print("=" * 70)

# Check 1: Environment variables
print("\n[CHECK 1] Environment Variables:")
api_key = os.environ.get('OPENROUTER_API_KEY')
print(f"  OPENROUTER_API_KEY present: {bool(api_key)}")
if api_key:
    print(f"  Key (first 20 chars): {api_key[:20]}...")
else:
    print("  [ERROR] API key not found!")

# Check 2: AI Service Import
print("\n[CHECK 2] AI Service Module:")
try:
    from app.ai_service import get_ai_client, OpenRouterAI
    print("  [OK] AI service module imported")
except Exception as e:
    print(f"  [ERROR] Failed to import: {e}")
    exit(1)

# Check 3: AI Client Initialization
print("\n[CHECK 3] AI Client Initialization:")
try:
    ai = get_ai_client()
    if ai:
        print(f"  [OK] AI client initialized")
        print(f"  API Key set: {bool(ai.api_key)}")
        print(f"  Model: {ai.model}")
        print(f"  API URL: {ai.api_url}")
    else:
        print("  [ERROR] AI client is None - API key likely not set")
except Exception as e:
    print(f"  [ERROR] Failed to initialize: {e}")

# Check 4: OpenRouter API Connection
print("\n[CHECK 4] OpenRouter API Connection:")
try:
    import requests
    
    if not api_key:
        print("  [SKIP] No API key to test")
    else:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:5000',
            'X-Title': 'Employee Management System'
        }
        payload = {
            'model': 'openrouter/auto',
            'messages': [{'role': 'user', 'content': 'Test connection. Reply with "Connected".'}],
            'temperature': 0.7,
            'max_tokens': 100
        }
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print(f"  HTTP Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0].get('message', {}).get('content', '')
                if content:
                    print(f"  [OK] API responding correctly")
                    print(f"  Response: {content[:50]}...")
                else:
                    print(f"  [WARN] Empty response content")
            else:
                print(f"  [ERROR] Unexpected response format")
        else:
            data = response.json() if response.text else {}
            print(f"  [ERROR] API error: {data}")
            
except requests.exceptions.Timeout:
    print("  [ERROR] API request timed out (30s)")
except requests.exceptions.ConnectionError as e:
    print(f"  [ERROR] Connection failed: {e}")
except Exception as e:
    print(f"  [ERROR] {e}")

# Check 5: Flask App Routes
print("\n[CHECK 5] Flask App and Routes:")
try:
    from app import create_app
    from app.models import db, Employee
    
    app = create_app('development')
    
    with app.test_client() as client:
        with app.app_context():
            emp = Employee.query.first()
            if emp:
                print(f"  [OK] Test employee found: {emp.name} (ID: {emp.id})")
                
                # Test login first
                print(f"\n  Testing protected endpoint with login...")
                r = client.post('/auth/login', data={
                    'email': 'admin@example.com',
                    'password': 'admin123'
                })
                
                # Try the API endpoint
                r = client.get(f'/api/ai/salary-recommendation/{emp.id}')
                print(f"  API Status: {r.status_code}")
                
                if r.status_code == 200:
                    data = r.get_json()
                    print(f"  Response keys: {list(data.keys())}")
                    if 'recommendation' in data:
                        rec = data['recommendation']
                        if rec and rec.strip():
                            print(f"  [OK] AI response received ({len(rec)} chars)")
                        else:
                            print(f"  [WARN] Empty recommendation")
                elif r.status_code == 503:
                    data = r.get_json()
                    print(f"  [ERROR] Service unavailable: {data.get('error', 'Unknown error')}")
                else:
                    print(f"  [ERROR] Unexpected status: {r.status_code}")
            else:
                print("  [WARN] No test employee found")
                
except Exception as e:
    print(f"  [ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE".center(70))
print("=" * 70)
