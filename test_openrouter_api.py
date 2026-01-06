"""Test OpenRouter API connection directly."""
import os
from dotenv import load_dotenv
load_dotenv()

import requests

api_key = os.environ.get('OPENROUTER_API_KEY')
print(f'API Key present: {bool(api_key)}')
print(f'API Key (first 20 chars): {api_key[:20] if api_key else "NONE"}...')

# Simple test
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'HTTP-Referer': 'http://localhost:5000',
    'X-Title': 'Employee Management System'
}

payload = {
    'model': 'openrouter/auto',
    'messages': [{'role': 'user', 'content': 'Hello, just testing this connection. Say "Connected" if you can read this.'}],
    'temperature': 0.7,
    'max_tokens': 100
}

print('\nTesting OpenRouter API connection...')
try:
    response = requests.post('https://openrouter.ai/api/v1/chat/completions', json=payload, headers=headers, timeout=30)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')
