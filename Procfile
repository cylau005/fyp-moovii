release: sed -i 's/managed = False/managed = True/' mysite/models.py
release: python3 manage.py migrate --fake mysite zero
release: python3 manage.py migrate mysite
release: python3 manage.py migrate
web: gunicorn mysite.wsgi
