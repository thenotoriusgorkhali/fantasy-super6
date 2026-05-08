#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth.models import User
User.objects.filter(username='admin').delete()
User.objects.create_superuser('admin', 'admin@fantasy.com', 'admin123')
"