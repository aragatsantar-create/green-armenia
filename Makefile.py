start:
	python manage.py migrate
	python create_admin.py
	python manage.py collectstatic --noinput
	gunicorn charity_site.wsgi:application