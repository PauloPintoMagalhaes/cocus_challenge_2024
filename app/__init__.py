from flask import Flask

from config.constants import UPLOAD_FOLDER

from .routes import routes


def create_app(config_name="default"):
    app = Flask(__name__)
    # app.config.from_pyfile("../config.py")
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.register_blueprint(routes)

    return app
