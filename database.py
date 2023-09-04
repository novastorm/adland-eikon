import logging
import os

from sqlalchemy import create_engine


def connect_db():
    logging.info("Connecting to database")
    connection_uri = "postgresql://{username}:{password}@{host}:{port}/{db}".format(
        username=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        db=os.environ.get("POSTGRES_DB"),
    )

    engine = create_engine(connection_uri)
    engine.connect()

    return engine
