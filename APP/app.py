""" Server package """
from flask import Flask
from .config import *
from .controllers.users.loginmanager import *
from .extensions import *
from .settings import configure_template, configure_extensions

# For " Import * "
__all__ = ['create_app']


def create_app(config_class=None):
    """ Create a Flask app """
    configuration = DevelopmentConfig if config_class is None else config_class

    app = Flask(__name__)
    app.config.from_object(configuration)

    with app.app_context():
        configure_extensions(app, extensions_list)

        from APP.controllers.main import main
        from APP.controllers.users import users
        from APP.controllers.api import api
        from APP.controllers.errors import errors
        app.register_blueprint(main)
        app.register_blueprint(users)
        app.register_blueprint(api)
        app.register_blueprint(errors)

        configure_template(app)

    return app
