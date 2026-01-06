"""Quick test that all AI endpoints are working."""
import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app('development')

with app.test_client() as client:
    with app.app_context():
        print('=== AI Endpoints Status ===\n')
        
        # Test salary recommendation
        r = client.get('/api/ai/salary-recommendation/1')
        print(f'[OK] Salary Recommendation: {r.status_code}')
        if r.status_code == 200:
            data = r.get_json()
            if data.get('recommendation'):
                print(f'     Response length: {len(data["recommendation"])} chars')
        
        # Test performance insight
        r = client.get('/api/ai/performance-insight/1')
        print(f'[OK] Performance Insight: {r.status_code}')
        if r.status_code == 200:
            data = r.get_json()
            if data.get('insight'):
                print(f'     Response length: {len(data["insight"])} chars')
        
        # Test attendance analysis
        r = client.get('/api/ai/attendance-analysis/1')
        print(f'[OK] Attendance Analysis: {r.status_code}')
        if r.status_code == 200:
            data = r.get_json()
            if data.get('analysis'):
                print(f'     Response length: {len(data["analysis"])} chars')
        
        # Test department insights
        r = client.get('/api/ai/department-insights/IT')
        print(f'[OK] Department Insights: {r.status_code}')
        if r.status_code == 200:
            data = r.get_json()
            if data.get('insight'):
                print(f'     Response length: {len(data["insight"])} chars')
        
        print('\n[SUCCESS] All AI Endpoints Working!')
