import re
from threading import Thread
from flask import url_for, current_app, render_template
from flask_mail import Message
from ..extensions import mail
from ..settings import DEFAULT_AUTHENTICATION_EMAIL_TEMPLATE, DEFAULT_EMAIL_SENDER


def send_email(subject, body, recipients, sender=DEFAULT_EMAIL_SENDER):
    """ Send A text MAil """
    message = Message(subject, sender=sender, recipients=[recipients])
    message.body = body
    mail.send(message)


def send_email_from_template(subject, template, recipients, sender=DEFAULT_EMAIL_SENDER, **kwargs):
    """ Send Email fromm Template """
    message = Message(subject, sender=sender, recipients=[recipients])
    message.html = render_template(template, **kwargs)
    mail.send(message)


def send_reset_email(user, template=DEFAULT_AUTHENTICATION_EMAIL_TEMPLATE):
    """ Sends Emil with Url That contains special token to reset user's password """
    token = user.get_reset_token()
    message = Message('Password Reset Request',
                      sender=DEFAULT_EMAIL_SENDER, recipients=[user.email])
    message.body = f'''To reset your password, visit the following link:
        {url_for('reset_token', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
        '''
    mail.send(message)


def send_confirmation_email(user, template=DEFAULT_AUTHENTICATION_EMAIL_TEMPLATE):
    """ Sends Emil with Url That contains special token to Confirm user's Emil """
    token = user.get_confirmation_token()
    message = Message('Email Confirmation',
                      sender=DEFAULT_EMAIL_SENDER, recipients=[user.email])
    # context = {}
    # message.html = render_template(template, **context)
    message.body = f'''To Confirm Your E-mail, visit the following link:
        {url_for('confirm_email', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
        '''
    mail.send(message)


def send_async_email(app, message):
    with app.app_context():
        mail.send(message)


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.html = html_body
    if attachments:
        for attachment in attachments:
            message.attach(*attachment)
    if sync:
        mail.send(message)
    else:
        Thread(target=send_async_email,
               args=(current_app._get_current_object(), message)).start()
