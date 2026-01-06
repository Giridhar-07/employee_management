"""Test salary recommendation with debug."""
import os
from dotenv import load_dotenv
load_dotenv()

import requests

# Direct API test first
print("=== Testing OpenRouter API Directly ===")
api_key = os.environ.get('OPENROUTER_API_KEY')
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'HTTP-Referer': 'http://localhost:5000',
    'X-Title': 'Employee Management System'
}
payload = {
    'model': 'openrouter/auto',
    'messages': [{'role': 'user', 'content': 'Analyze this employee salary: John Doe, Senior Developer, IT, 50000 monthly, 5 years exp. Is it competitive?'}],
    'temperature': 0.5,
    'max_tokens': 500
}

try:
    response = requests.post('https://openrouter.ai/api/v1/chat/completions', json=payload, headers=headers, timeout=30)
    print(f'Status: {response.status_code}')
    data = response.json()
    print(f'Full response: {data}')
    if response.status_code == 200:
        if 'choices' in data:
            content = data['choices'][0]['message']['content'].strip()
            print(f'Response: {content[:200]}...')
        else:
            print(f'No choices in response. Full response keys: {data.keys()}')
    else:
        print(f'Error response: {data}')
except Exception as e:
    print(f'Error: {e}')

print("\n=== Testing via AI Service ===")
from app.ai_service import get_ai_client

ai = get_ai_client()
print(f'AI Client available: {ai is not None}')

if ai:
    result = ai.get_salary_recommendation(
        'John Doe',
        'Senior Developer',
        'IT',
        50000,
        5
    )
    print(f'Recommendation: {result[:200] if len(result) > 200 else result}')
