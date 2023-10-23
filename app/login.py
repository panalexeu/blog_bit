from . import login_manager
from .models import User, AnonymousUser


login_manager.login_view = 'auth.login'  # setting base login view, which is called i.e. login required views
login_manager.anonymous_user = AnonymousUser  # adding our edited anonymous user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

