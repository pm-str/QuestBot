import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.config.settings")

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = os.environ['DJANGO_SU_USERNAME']
email = os.environ['DJANGO_SU_EMAIL']
password = os.environ['DJANGO_SU_PASS']

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(' SUPERUSER_CREATED '.center(100, '#'))
else:
    print(' SUPERUSER_EXISTS '.center(100, '#'))
