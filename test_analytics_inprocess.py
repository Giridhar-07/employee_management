from app import create_app, db
from app.models import Admin
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Ensure admin exists for tests
    admin = Admin.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = Admin(email='admin@example.com', username='admin', full_name='Admin User', is_active=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    admin_id = admin.id

with app.test_client() as c:
    # Force login by setting session
    with c.session_transaction() as sess:
        sess['admin_id'] = admin_id
        sess['admin_email'] = 'admin@example.com'
        sess['admin_username'] = 'admin'

    # analytics page
    r = c.get('/analytics')
    print('/analytics ->', r.status_code)

    # overview api
    r2 = c.get('/api/analytics/overview')
    print('/api/analytics/overview ->', r2.status_code)
    if r2.status_code==200:
        print('keys:', list(r2.json.keys()))
    else:
        print(r2.data[:200])
