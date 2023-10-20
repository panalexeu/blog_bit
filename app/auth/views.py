import flask
from flask_login import login_user
from . import auth
from .forms import LoginForm
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # User exists, password is correct hence we can log him in
            login_user(user, form.remember_me.data)

            # Redirection handling
            next_ = flask.request.args.get('next')
            if next_ is None or not next_.startswith('/'):
                # If next_ page doesn't exist or is malicious redirect to welcome page
                next_ = flask.url_for('main.welcome')
            return flask.redirect(next_)

    return flask.render_template('auth/login.html', form=form)
