# my_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Укажите имя вашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

app = Celery('school')

# Загрузка настроек из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
