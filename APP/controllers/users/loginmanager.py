""" Handling Loginmanager configrations """

from flask_login import UserMixin, AnonymousUserMixin
from ...extensions import login_manager
from ...controllers.users.models import UserModel


class AnonymousUser(AnonymousUserMixin):
    pass


login_manager.anonymous_user = AnonymousUser
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(session_token):
    return UserModel.query.filter_by(session_token=session_token).first()
