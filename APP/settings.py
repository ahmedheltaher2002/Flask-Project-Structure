import os

from .constants import APP_NAME
from .extensions import *

DEFAULT_EMAIL_DIRECTORY = 'emails/'
DEFAULT_EMAIL_TEMPLATES_DIRECTORY = DEFAULT_EMAIL_DIRECTORY + 'templates'
DEFAULT_EMAIL_TEXT_DIRECTORY = DEFAULT_EMAIL_DIRECTORY + 'text'

DEFAULT_AUTHENTICATION_EMAIL_TEMPLATE = DEFAULT_EMAIL_TEMPLATES_DIRECTORY + \
    'authentication_template.html'

DEFAULT_EMAIL_SENDER = 'norplay@APP.com'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = 'sqlite:///../../site.db'
ALLOWED_AVATAR_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'webp']

NAV_LINKS = {
    'authintacted': [],
    'notauthintacted': []
}

main_context = {
    'title': '',
    'show_navbar': False
}


def configure_template(app):
    app.add_template_global(name='APP_NAME', f=APP_NAME)
    app.add_template_global(name='NAV_LINKS', f=NAV_LINKS)


def configure_extensions(app, extensions=[db, hash_manager, login_manager, mail, toolbar]):
    for extension in extensions:
        extension.init_app(app)


