from flask import render_template, make_response, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from . import main
from .forms import PostForm
from .. import db
from ..decorators import permission_required
from ..models import Post, Permission


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
    show_post = request.cookies.get('show_post')
    if current_user.is_authenticated:
        if show_post == 'followed':
            query = current_user.followed_posts
        elif show_post == 'liked':
            query = current_user.liked_posts
        else:
            query = Post.query
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
                           show_post=show_post)


@main.route('/all')
def show_all():
    response = make_response(redirect(url_for('main.welcome')))
    response.set_cookie('show_post', '', max_age=60 * 60 * 24 * 30)  # max age of cookie is set for 30 days
    return response


@main.route('/followed')
@login_required
def show_followed():
    response = make_response(redirect(url_for('main.welcome')))
    response.set_cookie('show_post', 'followed', max_age=60 * 60 * 24 * 30)
    return response


@main.route('/liked')
@login_required
def show_liked():
    response = make_response(redirect(url_for('main.welcome')))
    response.set_cookie('show_post', 'liked', max_age=60 * 60 * 24 * 30)
    return response


@main.route('/preact_test')
@login_required
@permission_required(Permission.ADMIN)
def preact_test():
    return render_template('main/preact_test.html')
