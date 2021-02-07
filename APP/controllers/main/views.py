from flask import Blueprint, flash, render_template
from flask_login import current_user

from ...settings import main_context
from ...utils.dictionaries import copy_dict

main = Blueprint('main', __name__)


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_last_seen()


@main.route('/')
def home():
    context = copy_dict(main_context, {
        'title': 'Home',
        'show_navbar': True
    })
    flash('Login Unsuccessful. Please check the Email and password', 'danger')
    return render_template(f'main/index.html', **context)
