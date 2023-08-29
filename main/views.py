from flask import Blueprint, jsonify

from tasks import etl

main_blueprint = Blueprint("main", __name__)


# Your API that can be called to trigger your ETL process
@main_blueprint.route("/trigger_etl", methods=["POST"])
def trigger_etl():
    # Trigger your ETL process here
    etl.delay()
    return jsonify({"message": "ETL process started"}), 200
