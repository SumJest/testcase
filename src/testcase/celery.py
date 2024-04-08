import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testcase.settings')

app = Celery('testcase')
app.conf.broker_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0'

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
