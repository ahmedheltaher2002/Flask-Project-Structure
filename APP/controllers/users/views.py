from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from ...controllers.users.forms import *
from ...utils.emails import send_reset_email
from .models import UserModel, register_user
from ...extensions import db
from ...settings import main_context
from ...utils.dictionaries import copy_dict

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        register_user(first_name=register_form.first_name.data, last_name=register_form.last_name.data,
                      username=register_form.username.data, email=register_form.email.data,
                      password=register_form.password.data)
        flash(
            f'Account created for { register_form.username.data }!', 'success')
        return redirect(url_for('users.login'))
    context = copy_dict(main_context, {
        'title': 'Register',
        'form': register_form
    })
    return render_template('users/auth/register.html', **context)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = UserModel.query.filter_by(email=login_form.email.data).first()
        if user:
            if user.check_password(login_form.password.data):
                login_user(user, remember=login_form.remember.data)
                user.update_last_seen()
                next_page = request.args.get('next')
                flash(
                    f'Login successful. welcome Back {user.username}', 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash(
                    'Login Unsuccessful. Please check the Email and password', 'danger')
                return redirect(url_for('users.login'))
        else:
            return redirect(url_for('users.login'))
    context = copy_dict(main_context, {
        'title': 'Login',
        'form': login_form,
    })
    return render_template('users/auth/login.html', **context)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = current_user if (current_user.username == username) else UserModel.query.filter_by(
        username=username).first_or_404()
    context = copy_dict(main_context, {
        'user': user,
        'title': f'{user.username}\'s Profile',
        'is_yourself': True if (user == current_user) else False,
        'show_navbar': True
    })
    return render_template('users/profile.html', **context)


@users.route('/password_check', methods=['GET', 'POST'])
def password_check():
    password_check_form = PasswordCheckForm()
    context = copy_dict(main_context, {
        'title': 'Confirm Password',
        'form': password_check_form
    })
    return render_template('users/auth/password_check.html', **context)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    request_reset_form = RequestResetForm()
    if request_reset_form.validate_on_submit():
        user = UserModel.query.filter_by(
            email=request_reset_form.email.data).first()
        send_reset_email(user)
        flash('An Email has been Sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    context = copy_dict(main_context, {
        'title': 'Reset Password',
        'form': request_reset_form
    })
    return render_template('users/auth/reset_request.html', **context)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = UserModel.verify_token(token, 'recover-key')
    if user is None:
        flash('This is invalid or Expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    reset_password_form = ResetPasswordForm()
    if reset_password_form.validate_on_submit():
        user.update_password(reset_password_form.password.data)
        db.session.commit()
        flash(f'Your Password has been Updated!, Now you can login With the new password', 'success')
        return redirect(url_for('main.home'))
    context = copy_dict(main_context, {
        'title': 'Reset Password',
        'form': reset_password_form
    })
    return render_template('users/auth/reset_token.html', **context)


@users.route('/send_confirmation_email', methods=['GET', 'POST'])
def send_confirmation_email():
    send_confirmation_email_form = SendConfirmationEmailForm()
    if send_confirmation_email_form.validate_on_submit():
        user = UserModel.query.filter_by(email=current_user.email).first()
        send_confirmation_email(user)
        flash('An Email has been Sent with instructions to reset your password', 'info')
        return redirect(url_for('main.home'))
    context = copy_dict(main_context, {
        'title': 'Send Confirmation Email',
        'form': send_confirmation_email_form,
        'show_navbar': True
    })
    return render_template('users/auth/send_confirmation_email.html', **context)


@users.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    user = UserModel.verify_token(token, 'email-confirm-key')
    if user is None:
        flash('This is invalid or Expired token', 'warning')
        return redirect(url_for('users.send_confirmation_email'))
    else:
        user.confirm_email()
        db.session.commit()
        flash(f'Your Email Have been Confirmed', 'success')
        return redirect(url_for('main.home'))
    # context = copy_dict(main_context, {
    #     'title': 'Reset Password'
    # })
    # return render_template('users/auth/confirm_email.html', **context)
