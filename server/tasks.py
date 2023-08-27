import logging
import os

from celery import Celery

celery_app = Celery(__name__)

celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379"
)
celery_app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery_app.task(name="etl")
def etl():
    logging.debug("ETL process started")
    # Load CSV files
    # Process files to derive features
    # Upload processed data into a database
    logging.debug("ETL process completed")
