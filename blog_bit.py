import os
import sys
import click

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


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Runs tests under code coverage.')
def test(coverage):
    COV = None

    if coverage:
        import coverage
        COV = coverage.coverage(branch=True, include='app/*')
        COV.start()

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()

        print("Coverage Summary:")
        COV.report()

        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'reports\\coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file:\\\\%s\\index.html' % covdir)
        COV.erase()
