import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    from server.main.views import main_blueprint

    app.register_blueprint(main_blueprint)

    app.shell_context_processor({"app": app})

    return app
