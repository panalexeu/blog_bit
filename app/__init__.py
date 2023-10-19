from flask import Flask
from flask_bootstrap import Bootstrap

from .main import main as main_blueprint


# App factory
def create_app():
    app = Flask(__name__)

    # Initializing extensions
    Bootstrap().init_app(app)

    # Registering blueprint
    app.register_blueprint(main_blueprint)

    return app
