"""AI Service using OpenRouter API for intelligent features.
Integrates GPT-OSS-120B for salary recommendations, performance insights, and analysis.
"""
import os
import requests
import json
from functools import lru_cache

class OpenRouterAI:
    """OpenRouter AI client for intelligent employee insights."""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENROUTER_API_KEY')
        self.model = 'openrouter/auto'  # Will use GPT-OSS-120B (free)
        self.api_url = 'https://openrouter.ai/api/v1/chat/completions'
        if not self.api_key:
            raise ValueError('OPENROUTER_API_KEY not set in .env')
    
    def _call_api(self, messages, temperature=0.7):
        """Make a request to OpenRouter API."""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:5000',
                'X-Title': 'Employee Management System'
            }
            payload = {
                'model': self.model,
                'messages': messages,
                'temperature': temperature,
                'max_tokens': 500
            }
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                choice = data['choices'][0]
                message = choice.get('message', {})
                content = message.get('content', '').strip()
                
                # If content is empty but there's reasoning (some models), use that
                if not content and 'reasoning' in message:
                    content = message['reasoning'].strip()
                
                # Limit response to 500 characters for UI
                return content[:500] if content else None
            return None
        except requests.exceptions.RequestException as e:
            print(f'OpenRouter API error: {str(e)}')
            return None
        except Exception as e:
            print(f'Unexpected error in AI call: {str(e)}')
            return None
    
    def get_salary_recommendation(self, employee_name, position, department, current_salary, years_exp=None):
        """Get AI-powered salary recommendation."""
        prompt = f"""Analyze this employee's salary based on market standards and provide a brief recommendation.

Employee: {employee_name}
Position: {position}
Department: {department}
Current Salary: ${current_salary:,.2f}/month
Years of Experience: {years_exp or 'Unknown'}

Provide a brief recommendation (2-3 sentences) on whether the salary is competitive, below market, or above market. Be concise."""
        
        messages = [{'role': 'user', 'content': prompt}]
        return self._call_api(messages, temperature=0.5) or "Unable to generate recommendation at this time."
    
    def get_performance_insight(self, employee_name, department, attendance_score, months_employed):
        """Get AI-powered performance insight."""
        prompt = f"""Provide a brief professional insight on this employee's performance and engagement.

Employee: {employee_name}
Department: {department}
Attendance Score: {attendance_score}% (0-100)
Months Employed: {months_employed}

Provide 2-3 sentences assessing their engagement level and suggesting areas for improvement or recognition. Be constructive and professional."""
        
        messages = [{'role': 'user', 'content': prompt}]
        return self._call_api(messages, temperature=0.5) or "Unable to generate insight at this time."
    
    def get_attendance_analysis(self, employee_name, present_days, absent_days, total_days):
        """Analyze attendance patterns."""
        attendance_pct = (present_days / total_days * 100) if total_days > 0 else 0
        prompt = f"""Analyze this employee's attendance pattern and provide actionable feedback.

Employee: {employee_name}
Present Days: {present_days}
Absent Days: {absent_days}
Total Days: {total_days}
Attendance Rate: {attendance_pct:.1f}%

Provide 2-3 sentences analyzing trends and suggestions. Be professional and fair."""
        
        messages = [{'role': 'user', 'content': prompt}]
        return self._call_api(messages, temperature=0.5) or "Unable to generate analysis at this time."
    
    def get_department_insights(self, department_name, total_employees, avg_salary, avg_attendance):
        """Get insights for a department."""
        prompt = f"""Provide a brief strategic insight on this department's performance and health.

Department: {department_name}
Total Employees: {total_employees}
Average Salary: ${avg_salary:,.2f}/month
Average Attendance: {avg_attendance:.1f}%

Provide 2-3 sentences on department strength and areas for improvement. Be strategic and constructive."""
        
        messages = [{'role': 'user', 'content': prompt}]
        return self._call_api(messages, temperature=0.5) or "Unable to generate insight at this time."


# Global instance
_ai_client = None

def get_ai_client():
    """Get or create the AI client singleton."""
    global _ai_client
    try:
        if _ai_client is None:
            _ai_client = OpenRouterAI()
        return _ai_client
    except ValueError:
        # API key not set
        return None

def is_ai_enabled():
    """Check if AI is enabled."""
    return get_ai_client() is not None
