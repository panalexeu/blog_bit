from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from config import configs


bootstrap = Bootstrap()
db = SQLAlchemy()


# App factory
def create_app(config_name):
    # App init and configs setting
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    # Initializing extensions
    bootstrap.init_app(app)
    db.init_app(app)

    # Registering blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
