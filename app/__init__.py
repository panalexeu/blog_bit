from flask import Flask
from flask_bootstrap import Bootstrap

from .main import main as main_blueprint
from .auth import auth as auth_blueprint


# App factory
def create_app():
    app = Flask(__name__)

    # Initializing extensions
    Bootstrap().init_app(app)

    # Registering blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Configs
    app.config['SECRET_KEY'] = 'alexeu 2000004'

    return app
