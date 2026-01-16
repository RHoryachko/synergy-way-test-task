from celery import Celery

from app.config import settings

celery_app = Celery(
    "synergy_app",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "fetch-users": {
        "task": "app.tasks.fetch_users",
        "schedule": 300.0,
    },
    "fetch-posts": {
        "task": "app.tasks.fetch_posts",
        "schedule": 600.0,
        "kwargs": {"limit": 10},
    },
    "fetch-comments": {
        "task": "app.tasks.fetch_comments",
        "schedule": 600.0,
        "kwargs": {"limit": 10},
    },
}

from app import tasks
