import logging
import os

import pandas as pd
from celery import Celery

from database import connect_db

celery_app = Celery(__name__)

celery_app.config_from_object(os.getenv("APP_SETTINGS", "config.development"))

def extract(data_path):
    sep = ",\t"
    # Load CSV files
    users_df = pd.read_csv(f"{data_path}/users.csv", engine="python", sep=sep)
    user_experiments_df = pd.read_csv(
        f"{data_path}/user_experiments.csv", engine="python", sep=sep
    )
    compounds_df = pd.read_csv(f"{data_path}/compounds.csv", engine="python", sep=sep)

    return {
        "users_df": users_df,
        "user_experiments_df": user_experiments_df,
        "compounds_df": compounds_df
    }

def transform(data):
    total_experiments_per_user = data['user_experiments_df'].groupby("user_id").agg(
        {"experiment_id": {len}}
    )
    logging.debug("total_experiments_per_user")
    logging.debug(total_experiments_per_user)

    avg_experiments_per_user = total_experiments_per_user["experiment_id"].mean()
    logging.debug("avg_experiments_per_user")
    logging.debug(avg_experiments_per_user)

    most_experimented_compound = data['user_experiments_df'].copy()
    most_experimented_compound["experiment_compound_ids"] = most_experimented_compound[
        "experiment_compound_ids"
    ].str.split(";")

    most_experimented_compound_id = (
        most_experimented_compound["experiment_compound_ids"]
        .explode()
        .value_counts()
        .reset_index()
        .iloc[0]["index"]
    )
    a_filter = data['compounds_df']["compound_id"].values == int(
        most_experimented_compound_id
    )
    most_experimented_compound = data['compounds_df'][a_filter]

    logging.debug("most_experimented_compound")
    logging.debug(most_experimented_compound)

    return {
        "total_experiments_per_user": total_experiments_per_user,
        "avg_experiments_per_user": avg_experiments_per_user,
        "most_experimented_compound": most_experimented_compound,
    }

def load_experiements_per_user_to_db(dataframe):
    engine = connect_db()
    dataframe.to_sql("experiments_per_user", con=engine, if_exists="replace")

@celery_app.task(name="etl")
def etl():
    base_dir = os.path.dirname(__file__)
    data_dir = os.environ.get("DATA_DIR", "data")
    data_path = os.path.join(base_dir, data_dir)
    logging.debug("ETL process started")
    # Load CSV files
    data = extract(data_path)

    # Process files to derive features
    t_data = transform(data)
    total_experiments_per_user = t_data["total_experiments_per_user"]
    avg_experiments_per_user = t_data["avg_experiments_per_user"]
    most_experimented_compound = t_data["most_experimented_compound"]


    # 1. Total number of experiments ran by each user.
    # 2. Average number of experiments per user.
    # 3. User's most commonly experimented compound.

    # Upload processed data into a database
    load_experiements_per_user_to_db(total_experiments_per_user)

    logging.debug("ETL process completed")
