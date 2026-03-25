import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feature_requests.settings')


def pytest_configure():
    django.setup()
