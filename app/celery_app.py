import sys

from celery import Celery

from app.config import CELERY_BROKER_URL

celery_app = Celery("upload_doc", broker=CELERY_BROKER_URL)

if sys.platform == "win32":
    celery_app.conf.worker_pool = "solo"

import app.tasks  # noqa: F401, E402
