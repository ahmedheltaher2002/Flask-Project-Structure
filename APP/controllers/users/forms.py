import wtforms
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from .models import UserModel
from APP.settings import ALLOWED_AVATAR_EXTENSIONS

__all__ = ['RegistrationForm', 'LoginForm', 'PasswordCheckForm', 'UpdateAccountForm', 'RequestResetForm',
           'ResetPasswordForm', 'ChangePasswordForm', 'ChangeEmailForm', 'SendConfirmationEmailForm']


def password_validator(password):
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password should have at least one number')

    if not any(char.isupper() for char in password):
        raise ValidationError(
            'Password should have at least one uppercase letter')

    if not any(char.islower() for char in password):
        raise ValidationError(
            'Password should have at least one lowercase letter')


class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[
                             DataRequired(), Length(min=2, max=128)])
    last_name = StringField("Last Name", validators=[
                            DataRequired(), Length(min=2, max=128)])
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=8, max=256)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That Username is already Taken, Please choose another one")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That Email is already Taken, Please choose another one')

    def validate_password(self, password):
        password_validator(password.data)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField("First Name", validators=[
                             DataRequired(), Length(min=2, max=128)])
    last_name = StringField("Last Name", validators=[
                            DataRequired(), Length(min=2, max=128)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=8, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Ptofile Picture', validators=[
                        FileAllowed(ALLOWED_AVATAR_EXTENSIONS)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = UserModel.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is already Taken, Please choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = UserModel.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That Email is already Taken, Please choose another one')


class PasswordCheckForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register Right Now.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[
                                     DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

    def validate_password(self, password):
        password_validator(password.data)


class ChangeEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Change Email')

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user:
            if email == user.email:
                raise ValidationError(
                    'The new email can\'t be the same as your current one')
            else:
                raise ValidationError(
                    'That Email is already Taken, Please choose another one')


class SendConfirmationEmailForm(FlaskForm):
    submit = SubmitField('Send')
