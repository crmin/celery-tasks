import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beringlab.settings')
app = Celery('tasks')

# 별도의 settings 값이 있는 경우 settings에서 CELERY_* 설정 값을 읽어서 반영
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # app directory 아래의 celery task를 검색
