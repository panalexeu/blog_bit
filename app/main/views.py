from flask_login import login_required, current_user
from flask import render_template, abort, flash, make_response, redirect, url_for, request, current_app

from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from ..models import User, Role, Post, Permission, Follow, Comment
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

    # if showing posts of only followed users set
    show_followed = request.cookies.get('show_followed')
    if show_followed and current_user.is_authenticated:
        query = current_user.followed_posts
    else:
        query = Post.query

    # Posts paginating implementation
    page = request.args.get('page', default=1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
    )
    posts = pagination.items

    return render_template('main/welcome.html', form=form, posts=posts, pagination=pagination,
                           show_followed=show_followed)


@main.route('/all')
def show_all():
    response = make_response(redirect(url_for('main.welcome')))
    response.set_cookie('show_followed', '', max_age=60 * 60 * 24 * 30)  # max age of cookie is set for 30 days
    return response


@main.route('/followed')
@login_required
def show_followed():
    response = make_response(redirect(url_for('main.welcome')))
    response.set_cookie('show_followed', '1', max_age=60 * 60 * 24 * 30)
    return response


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

        flash('Your profile has been updated.', 'success')

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

        flash('User profile has been changed.', 'success')

        return redirect(url_for('main.profile', username=user.username))

    form.name.data = user.name
    form.about_me.data = user.about_me
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role

    return render_template('main/edit_profile.html', form=form)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data,
            post=post,
            author=current_user._get_current_object()
        )

        db.session.add(comment)
        db.session.commit()

        flash('Your comment has been published.', 'success')

        return redirect(url_for('main.post', id=post.id))

    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['COMMENTS_PER_PAGE']
    )
    comments = pagination.items

    return render_template('main/post.html', posts=[post], form=form, comments=comments, pagination=pagination)


@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)

    if current_user != post.author and not current_user.is_administrator():
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()

        flash('The post has been updated.', 'success')

        return redirect(url_for('main.post', id=post.id))

    form.body.data = post.body

    return render_template('main/edit_post.html', form=form)


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


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', default=1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['COMMENTS_PER_PAGE']
    )
    comments = pagination.items

    return render_template('main/moderate.html', comments=comments, page=page, pagination=pagination)


@main.route('/moderate-comment/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_comment_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False

    db.session.add(comment)
    db.session.commit()

    # if comment moderation was performed in post page and not moderate page
    if 'post' in request.referrer:
        return redirect(url_for('main.post', id=comment.post_id, page=request.args.get('page', default=1, type=int)))
    else:
        return redirect(url_for('main.moderate', page=request.args.get('page', default=1, type=int)))


@main.route('/moderate-comment/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_comment_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True

    db.session.add(comment)
    db.session.commit()

    # if comment moderation was performed in post page and not moderate page
    if 'post' in request.referrer:
        return redirect(url_for('main.post', id=comment.post_id, page=request.args.get('page', default=1, type=int)))
    else:
        return redirect(url_for('main.moderate', page=request.args.get('page', default=1, type=int)))


@main.route('/moderate-post/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_post_enable(id):
    post = Post.query.get_or_404(id)
    post.disabled = False

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('main.post', id=post.id))


@main.route('/moderate-post/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_post_disable(id):
    post = Post.query.get_or_404(id)
    post.disabled = True

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('main.post', id=post.id))


@main.route('/upgrade-to-mod/<int:id>')
@login_required
@admin_required
def upgrade_to_mod(id):
    user = User.query.get_or_404(id)
    user.role = Role.query.filter_by(name='Moderator').first()
    db.session.commit()

    flash('User profile has been upgraded to Moderator.', 'warning')

    return redirect(url_for('main.profile', username=user.username))


@main.route('/downgrade-mod/<int:id>')
@login_required
@admin_required
def downgrade_mod(id):
    user = User.query.get_or_404(id)
    user.role = Role.query.filter_by(name='User').first()
    db.session.commit()

    flash('User profile has been downgraded to User.', 'warning')

    return redirect(url_for('main.profile', username=user.username))
