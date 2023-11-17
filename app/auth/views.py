import flask
import flask_login

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..email import send_email
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # User exists, password is correct hence we can log him in
            flask_login.login_user(user, form.remember_me.data)

            # Redirection handling
            next_ = flask.request.args.get('next')
            if next_ is None or not next_.startswith('/'):
                # If next_ page doesn't exist or is malicious - redirect to welcome page
                next_ = flask.url_for('main.welcome')

            return flask.redirect(next_)
        else:
            flask.flash('Invalid email or password.', 'error')

    return flask.render_template('auth/login.html', form=form)


@auth.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flask.flash('You have been logged out.', 'success')
    return flask.redirect(flask.url_for('main.welcome'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Adding user to db
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        user.follow(user)  # making user follow himself
        db.session.commit()

        # Confirmation token generation and email sending
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your account', 'confirm', username=user.username, token=token)
        flask.flash('A confirmation email has been sent to you by email.', 'success')

        return flask.redirect(flask.url_for('auth.login'))

    return flask.render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@flask_login.login_required
def confirm(token):
    if flask_login.current_user.confirmed:
        return flask.redirect(flask.url_for('main.welcome'))
    elif flask_login.current_user.confirm(token, expiration=3600):  # expiration is set in seconds 3600 = 1 hour
        flask.flash('You have confirmed your account. Thanks!', 'success')
    else:
        flask.flash('The confirmation link is invalid or has expired.', 'error')

    return flask.redirect(flask.url_for('main.welcome'))


@auth.route('/reconfirm')
@flask_login.login_required
def reconfirm():
    current_user = flask_login.current_user

    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm your account', 'confirm', username=current_user.username, token=token)
    flask.flash('A new confirmation email has been sent to you by email.', 'warning')

    return flask.redirect(flask.url_for('main.welcome'))


@auth.before_app_request
def before_request():
    current_user = flask_login.current_user
    if current_user.is_authenticated:
        current_user.ping()  # updating user last time seen property
        if not current_user.confirmed \
                and flask.request.blueprint != 'auth' \
                and flask.request.endpoint != 'static':
            return flask.redirect(flask.url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    current_user = flask_login.current_user

    if current_user.is_anonymous or current_user.confirmed:
        return flask.redirect(flask.url_for('main.welcome'))

    return flask.render_template('auth/unconfirmed.html', username=current_user.username)
