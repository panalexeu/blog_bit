from flask import jsonify
from flask_login import login_required, current_user

from . import main
from ..decorators import permission_required
from ..models import Post, Permission


@main.route('/like-post/<int:id>')
@login_required
@permission_required(Permission.LIKE)
def like_post(id):
    post = Post.query.get_or_404(id)
    current_user.like(post)
    return jsonify({'success': True})


@main.route('/unlike-post/<int:id>')
@login_required
@permission_required(Permission.LIKE)
def unlike_post(id):
    post = Post.query.get_or_404(id)
    current_user.unlike(post)
    return jsonify({'success': True})
