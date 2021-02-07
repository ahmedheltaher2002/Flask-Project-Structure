from flask import current_app, url_for
from ...extensions import db, hash_manager
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer, URLSafeSerializer


def register_user(first_name, last_name, username, email, password):
    """ Register a new user """
    user = UserModel(first_name=first_name, last_name=last_name,
                username=username, email=email)
    user.set_password(password)
    user.session_token = user.generate_session_token(
        email, user.generate_hashed_password(password))
    db.session.add(user)
    db.session.commit()


class UserModel(db.Model, UserMixin):
    """
    User
    ====
    User Module which Contains All Users Data
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    session_token = db.Column(db.String(256), unique=True, nullable=False)
    last_seen = db.Column(db.DateTime, nullable=True)

    def get_reset_token(self, expire_seconds=1800):
        """ Generates a Random token that have expiry duration of 30 minutes To Reset User's Password """
        serializer = TimedJSONWebSignatureSerializer(
            current_app.config["SECRET_KEY"], expire_seconds)
        return serializer.dumps(self.email, salt='recover-key')

    def get_confirmation_token(self, expire_seconds=3600):
        """ Generates a Random token that have expiry duration of 60 minutes To Confirm That the user's E-mail Is Valid """
        serializer = TimedJSONWebSignatureSerializer(
            current_app.config["SECRET_KEY"], expire_seconds)
        return serializer.dumps(self.email, salt='email-confirm-key')

    def generate_session_token(self, email, password):
        """ Generates a session token from user login information """
        serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps([email, password])

    def generate_hashed_password(self, password):
        """ Generates a Hashed Password """
        return hash_manager.generate_password_hash(password).decode('utf-8')

    def get_id(self):
        """ Return User session token which genereted using user login information """
        return self.session_token

    def update_password(self, password):
        """ Sets The Passed password as users password after hashing it then updates the session token """
        serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
        self.password = self.generate_hashed_password(password)
        self.session_token = self.generate_session_token(
            self.email, self.password)
        db.session.commit()

    def update_email(self, email):
        """ Sets The Passed email as users email then updates the session token """
        serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
        self.email = email
        self.session_token = self.generate_session_token(email, self.password)
        self.settings.user_states = 0
        db.session.commit()

    def check_password(self, password):
        """ Check hashed password """
        return hash_manager.check_password_hash(self.password, password)

    def set_password(self, password):
        """ hash the password and sets it as users password """
        self.password = self.generate_hashed_password(password)
        db.session.commit()

    def full_name(self):
        return f'{self.first_name} {self.optional_infos.middle_name} {self.last_name}' if not (self.optional_infos.middle_name == '') else f'{self.first_name} {self.last_name}'

    def update_last_seen(self):
        """ Updates Last Login time for the user """
        self.last_seen = datetime.now()
        db.session.commit()

    def __repr__(self):
        return f"{self.full_name()}"

        
    @staticmethod
    def verify_token(token, loading_key):
        """ Checks if the Email token is still valid to reset user password """
        serializer = TimedJSONWebSignatureSerializer(
            current_app.config["SECRET_KEY"])
        try:
            user_id = serializer.load(token)[loading_key]
        except:
            return None
        return UserModel.query.get(user_id)
