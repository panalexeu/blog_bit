from flask import Blueprint

main = Blueprint('main', __name__)

from . import main_views, moderation_views, like_views, follow_views, post_views, profile_views, errors
