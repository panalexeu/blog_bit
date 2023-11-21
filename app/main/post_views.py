from flask import render_template, abort, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from . import main
from .forms import PostForm, CommentForm
from .. import db
from ..models import Post, Comment


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
