from flask import render_template

from . import main
from ..models import User


@main.route('/')
def welcome():
    return render_template('main/welcome.html')


@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/profile.html', user=user)