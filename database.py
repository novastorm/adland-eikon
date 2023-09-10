import logging
import os

from sqlalchemy import create_engine

config_import = __import__(os.getenv("APP_SETTINGS", "config.development"), fromlist=[None])
config = {
    "username": getattr(config_import, "POSTGRES_USERNAME", "postgres"),
    "password": getattr(config_import, "POSTGRES_PASSWORD", "password"),
    "host": getattr(config_import, "POSTGRES_HOST", "localhost"),
    "port": getattr(config_import, "POSTGRES_PORT", 5432),
    "database": getattr(config_import, "POSTGRES_DB", "postgres"),
}


def connect_db():
    logging.info("Connecting to database")

    connection_uri = "postgresql://{username}:{password}@{host}:{port}/{db}".format(
        username=config["username"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
        db=config["database"],
    )

    engine = create_engine(connection_uri)
    engine.connect()

    return engine
