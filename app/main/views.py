from flask_login import login_required, current_user
from flask import render_template, flash, redirect, url_for

from . import main
from .forms import EditProfileForm
from ..models import User
from .. import db


@main.route('/')
def welcome():
    return render_template('main/welcome.html')


@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/profile.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data

        db.session.add(current_user)
        db.session.commit()

        flash('Your profile has been updated.')

        return redirect(url_for('.profile', username=current_user.username))

    # fulfilling fields with previously saved data
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me

    return render_template('main/edit_profile.html', form=form)
