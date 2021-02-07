import os

from .settings import DATABASE_URL

# For " Import * "
__all__ = ['DevelopmentConfig', 'ProductionConfig']


class BaseConfig(object):
    '''
    Base config class
    '''
    SECRET_KEY = '748db19496ebaf3be684dd8110ef2fb04e4362ac100a0a6d824305ff3c05b054'
    SQLALCHEMY_DATABASE_URI = ''
    MAIL_SERVER = ''
    MAIL_PORT = ''
    MAIL_USE_TLS = ''
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    DEBUG = True
    TESTING = False
    DEBUG_TB_PROFILER_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class DevelopmentConfig(BaseConfig):
    """
    Development environment specific configuration
    """
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'yourmail@gmail.com'
    MAIL_PASSWORD = 'yourpassword'
    TESTING = True
    DEBUG_TB_PROFILER_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(BaseConfig):
    """
    Production specific config
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DEBUG = False
