import pandas as pd
from flask import Blueprint, jsonify

from database import connect_db
from tasks import etl

main_blueprint = Blueprint("main", __name__)


# Your API that can be called to trigger your ETL process
@main_blueprint.route("/trigger_etl", methods=["POST"])
def trigger_etl():
    # Trigger your ETL process here
    etl.delay()
    return jsonify({"message": "ETL process started"}), 200

@main_blueprint.route("/report", methods=["GET"])
def report():

    db = connect_db()

    total_experiments_per_user = pd.read_sql_query(
        "SELECT * FROM experiments_per_user", db
    )

    average_experiments_per_user = pd.read_sql_query(
        "SELECT * FROM avg_experiments_per_user", db
    )

    most_experimented_compound = pd.read_sql_query(
        "SELECT * FROM most_experimented_compound", db
    )

    return jsonify(
        {
            "total_experiments_per_user": total_experiments_per_user.to_dict(orient="records"),
            "average_experiments_per_user": average_experiments_per_user.to_dict(orient="records"),
            "most_experimented_compound": most_experimented_compound.to_dict(orient="records"),
        }
    )
