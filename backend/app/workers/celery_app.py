"""
Celery worker application instance.
Configures task queues, serialization, and Redis broker settings.
"""

from celery import Celery
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

celery_app = Celery(
    "hiresmart_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max per task
    result_expires=3600,  # Result kept for 1 hour
)

# Auto-discover tasks in workers module
celery_app.autodiscover_tasks(["app.workers"])
