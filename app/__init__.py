from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from config import configs


# Instantiating extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


# App factory
def create_app(config_name):
    # App init and configs setting
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    # Initializing extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Registering blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


from . import login
