import os

DATA_DIR = os.getenv("DATA_DIR", "data")
BROKER_URL = os.getenv("BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.getenv("RESULT_BACKEND", "redis://localhost:6379/0")
CELERY_TASKS_ALWAYS_EAGER = os.getenv("CELERY_TASKS_ALWAYS_EAGER", False)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 15432)
POSTGRES_USER = os.getenv("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
