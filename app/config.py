import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DOCUMENTS_DIR = BASE_DIR / "documents"

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//"
)

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "minioadmin")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "minioadmin")
S3_BUCKET = os.getenv("S3_BUCKET", "documents")
S3_REGION = os.getenv("S3_REGION", "us-east-1")
