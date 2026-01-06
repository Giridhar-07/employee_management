web: gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 4 --worker-class sync --timeout 60 --access-logfile - --error-logfile -
release: python -c "from app import create_app, db; app = create_app('production'); db.create_all()"
