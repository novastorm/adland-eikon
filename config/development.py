import os

DATA_DIR = os.getenv("DATA_DIR", "data")
broker_url = os.getenv("broker_url", "redis://localhost:6379/0")
result_backend = os.getenv("result_backend", "redis://localhost:6379/0")
task_always_eager = os.getenv("task_always_eager", False)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_USER = os.getenv("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
