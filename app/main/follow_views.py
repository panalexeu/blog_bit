from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from . import main
from ..decorators import permission_required
from ..models import User, Permission, Follow


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        flash("You can't follow yourself!", 'error')
        return redirect(url_for('main.welcome'))

    if current_user.is_following(user):
        flash('You are already following this user.', 'warning')
        return redirect(url_for('main.profile', username=username))

    current_user.follow(user)
    flash(f'You are now following {username}.', 'success')

    return redirect(url_for('main.profile', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        flash("You can't unfollow yourself!", 'error')
        return redirect(url_for('main.welcome'))

    if not current_user.is_following(user):
        flash('You are not following this user.', 'warning')
        return redirect(url_for('main.profile', username=username))

    current_user.unfollow(user)
    flash(f'You stopped following {username}.', 'success')

    return redirect(url_for('main.profile', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', default=1, type=int)
    pagination = user.followers.filter(Follow.follower_id != user.id).order_by(Follow.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
    )

    follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]

    return render_template('main/followers.html', user=user, follows=follows, pagination=pagination)


@main.route('/following/<username>')
def following(username):
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', default=1, type=int)
    # Get followers excluding the user
    pagination = user.followed.filter(Follow.followed_id != user.id).order_by(Follow.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
    )

    follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]

    return render_template('main/following.html', user=user, follows=follows, pagination=pagination)
