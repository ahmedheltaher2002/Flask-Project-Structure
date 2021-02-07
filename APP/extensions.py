from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

__all__ = ['db', 'hash_manager', 'hash_manager', 'login_manager', 'toolbar', 'mail', 'extensions_list']

toolbar = DebugToolbarExtension()
db = SQLAlchemy()
hash_manager = Bcrypt()
mail = Mail()
login_manager = LoginManager()


extensions_list = [db, hash_manager, hash_manager, login_manager, toolbar, mail]