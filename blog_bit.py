import os

from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Permission


app = create_app(os.getenv('FLASK_CONFIG', 'default'))  # instantiating the app
migrate = Migrate(app, db)  # to make migrations through terminal


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


@app.context_processor
def inject_permissions():
    return dict(Permission=Permission)  # to use permission in templates
