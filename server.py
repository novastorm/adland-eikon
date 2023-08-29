import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["BASE_DIR"] = os.path.dirname(__file__)
    app_settings = os.getenv("APP_SETTINGS", "config.development")
    app.config.from_object(app_settings)

    from main.views import main_blueprint

    app.register_blueprint(main_blueprint)

    @app.shell_context_processor
    def shell_context():
        return {"app": app}

    return app
