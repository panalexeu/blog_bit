from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import login_required

from . import main
from .. import db
from ..decorators import admin_required, permission_required
from ..models import User, Role, Post, Permission, Comment


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

    # db.session.add(comment)
    db.session.commit()

    return jsonify({'success': True})


@main.route('/moderate-comment/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_comment_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True

    # db.session.add(comment)
    db.session.commit()

    return jsonify({'success': True})


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

    flash(f'User {user.username} has been upgraded to Moderator.', 'success')

    return redirect(url_for('main.profile', username=user.username))


@main.route('/downgrade-mod/<int:id>')
@login_required
@admin_required
def downgrade_mod(id):
    user = User.query.get_or_404(id)

    user.role = Role.query.filter_by(name='User').first()
    db.session.commit()

    flash(f'User {user.username} has been downgraded to User.', 'success')

    return redirect(url_for('main.profile', username=user.username))


@main.route('/disable-user/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def disable_user(id):
    user = User.query.get_or_404(id)

    if user.is_mod():
        flash('You are not allowed to disable moderators!', category='error')
        return redirect(url_for('main.profile', username=user.username))

    user.role = Role.query.filter_by(name='Disabled').first()
    db.session.commit()

    flash(f'User {user.username} has been disabled.', 'warning')

    return redirect(url_for('main.profile', username=user.username))


@main.route('/enable-user/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def enable_user(id):
    user = User.query.get_or_404(id)

    if user.is_mod():
        flash('You are not allowed to disable moderators!', category='error')
        return redirect(url_for('main.profile', username=user.username))

    user.role = Role.query.filter_by(name='User').first()
    db.session.commit()

    flash(f'User {user.username} has been enabled.', category='warning')

    return redirect(url_for('main.profile', username=user.username))
