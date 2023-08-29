import os

DATA_DIR = os.getenv("DATA_DIR", "data")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
CELERY_TASKS_ALWAYS_EAGER = os.getenv("CELERY_TASKS_ALWAYS_EAGER", False)
