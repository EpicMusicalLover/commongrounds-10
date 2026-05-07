release: python commongrounds/manage.py collectstatic --noinput
web: gunicorn commongrounds.wsgi:application --bind 0.0.0.0:8000
