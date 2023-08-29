import logging
import os

import pandas as pd
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
    base_dir = os.path.dirname(__file__)
    data_dir = os.environ.get("DATA_DIR", "data")
    data_path = os.path.join(base_dir, data_dir)
    sep = ",\t"
    logging.debug("ETL process started")
    # Load CSV files
    users_df = pd.read_csv(f"{data_path}/users.csv", engine='python', sep=sep)
    user_experiments_df = pd.read_csv(f"{data_path}/user_experiments.csv", engine='python', sep=sep)
    compounds_df = pd.read_csv(f"{data_path}/compounds.csv", engine='python', sep=sep)

    # Process files to derive features
    # 1. Total number of experiments ran by each user.
    total_experiments_per_user = (
        user_experiments_df[["user_id", "experiment_id"]]
        .groupby("user_id")
        .size()
        .to_frame('number_of_experiments')
    )
    logging.debug("total_experiments_per_user")
    logging.debug(total_experiments_per_user)

    # 2. Average number of experiments per user.
    avg_experiments_per_user = total_experiments_per_user["experiment_id"].mean()

    logging.debug("avg_experiments_per_user")
    logging.debug(avg_experiments_per_user)

    # 3. User's most commonly experimented compound.
    # copy the dataframe and split the compound ids into a list
    most_exp_comp = user_experiments_df.copy()
    most_exp_comp["experiment_compound_ids"] = user_experiments_df["experiment_compound_ids"].str.split(";")
    most_exp_comp = most_exp_comp.groupby("user_id").agg({"experiment_compound_ids": sum})

    # calculate the most common compound used for each user
    most_exp_comp["most_common_compound"] = None
    for i, r in most_exp_comp.iterrows():
        compound_counts = pd.Series(r["experiment_compound_ids"]).value_counts()
        max_count = compound_counts[0]
        most_exp_comp.loc[i, "most_common_compound"] = list([ck for ck, cv in compound_counts.iteritems() if cv == max_count])

    most_experimented_compound_id_map = most_exp_comp["experiment_compound_ids"].explode().value_counts().reset_index().iloc[0]["index"]
    a_filter = compounds_df["compound_id"].values == int(most_experimented_compound_id_map)
    most_experimented_compound = compounds_df[a_filter]

    logging.debug("most_experimented_compound")
    logging.debug(most_experimented_compound)

    # Upload processed data into a database
    logging.debug("ETL process completed")
