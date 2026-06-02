"""
Storage package.

Keeps storage backends (S3/MinIO) and exposes them as a normal Python package.
"""

from . import s3_storage

__all__ = ["s3_storage"]
