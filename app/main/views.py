from flask_login import login_required, current_user
from flask import render_template, abort, flash, redirect, url_for, request, current_app

from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from ..models import User, Role, Post, Permission
from .. import db
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def welcome():
    form = PostForm()

    # User submitted new post
    if form.validate_on_submit():
        post = Post(
            body=form.body.data,
            author=current_user._get_current_object()
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('main.welcome'))

    # Posts paginating implementation
    page = request.args.get('page', default=1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
    )
    posts = pagination.items

    return render_template('main/welcome.html', form=form, posts=posts, pagination=pagination)


@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    # Posts paginating implementation
    page = request.args.get('page', default=1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
    )
    posts = pagination.items

    return render_template('main/profile.html', user=user, posts=posts, pagination=pagination)


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


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.about_me = form.about_me.data
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)

        db.session.add(user)
        db.session.commit()

        flash('User profile has been changed.')

        return redirect(url_for('main.profile', username=user.username))

    form.name.data = user.name
    form.about_me.data = user.about_me
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role

    return render_template('main/edit_profile.html', form=form)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('main/post.html', posts=[post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)

    if current_user != post.author and not current_user.is_administrator():
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()

        flash('The post has been updated.')

        return redirect(url_for('main.post', id=post.id))

    form.body.data = post.body

    return render_template('main/edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        flash("You can't follow yourself!")
        return redirect(url_for('main.welcome'))

    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('main.profile', username=username))

    current_user.follow(user)
    flash(f'You are now following {username}.')

    return redirect(url_for('main.profile', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        flash("You can't unfollow yourself!")
        return redirect(url_for('main.welcome'))

    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('main.profile', username=username))

    current_user.unfollow(user)
    flash(f'You stopped following {username}.')

    return redirect(url_for('main.profile', username=username))

# @main.route('/followers/<username>')
# def followers(username):
#     user = User.query.filter_by(username=username).first_or_404()
#
#     page = request.args.get('page', 1, type=int)
#     pagination = user.followers.paginate(
#         page=page,
#         per_page=current_app.config['POSTS_PER_PAGE'],
#     )
#     follows = pagination.items
#
#     return render_template(None)

