from dotenv import load_dotenv
load_dotenv()
from app import create_app

app = create_app('development')
with app.test_client() as c:
    r = c.get('/api/stats')
    print('status', r.status_code)
    print('data', r.get_data(as_text=True))
