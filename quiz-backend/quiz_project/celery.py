import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

app = Celery('quiz_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery configuration
app.conf.update(
    # Task routing
    task_routes={
        'users.tasks.*': {'queue': 'email'},
        'results.tasks.*': {'queue': 'results'},
        'quizzes.tasks.*': {'queue': 'quizzes'},
    },
    
    # Task serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Worker settings
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    
    # Result backend
    result_backend='redis://localhost:6379/1',
    
    # Beat schedule for periodic tasks
    beat_schedule={
        'cleanup-expired-sessions': {
            'task': 'quizzes.tasks.cleanup_expired_sessions',
            'schedule': 3600.0,  # Every hour
        },
        'update-analytics': {
            'task': 'results.tasks.update_analytics',
            'schedule': 3600.0,  # Every hour
        },
        'send-reminder-emails': {
            'task': 'users.tasks.send_reminder_emails',
            'schedule': 86400.0,  # Daily
        },
    },
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 