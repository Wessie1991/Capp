
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    Password = db.Column(db.Binary(60), nullable=False)
    login_session = db.Column(db.String(10), nullable=True)

    def __init__(self, email, plaintext_password, login_session):
        self.email = email
        self.Password =  bcrypt.generate_password_hash(plaintext_password)
        self.authenticated = False
        self.login_session = login_session

    @hybrid_property
    def password(self):
        return self.Password

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.Password, plaintext_password)


    def new_friend(self, email_friend):
        newfriend = Friendlist(email_users = self.email, email_users_friend = email_friend)
        db.session.add(newfriend)
        db.session.commit()

    # User Authentication fields
    #email = db.Column(db.String(255), nullable=False, unique=True)
    #email_confirmed_at = db.Column(db.DateTime())


    # User fields
    #active = db.Column(db.Boolean()),
    #first_name = db.Column(db.String(50), nullable=False)
    #last_name = db.Column(db.String(50), nullable=False)

class Friendlist(db.Model):
    __tableName__ = 'friendlist'
    id = db.Column(db.Integer, primary_key=True)
    email_users = db.Column(db.String(50), db.ForeignKey('users.email'),nullable=False)
    email_users_friend = db.Column(db.String(50), db.ForeignKey('users.email'),nullable=False)
    accept = db.Column(db.Boolean , nullable=True)
    chats = db.relationship('Chats', backref='Friendlist', lazy='dynamic')

    def new_message(self, users_send, users_receiver, message, flag):
        db.session.expunge_all()
        newmessage = Chats(id_Friendlist = self.id, users_send = users_send,
                           users_receiver = users_receiver, message=message,
                           see_flag = flag)
        db.session.add(newmessage)
        db.session.commit()


class Chats(db.Model):
    __tableName__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    id_Friendlist =  db.Column(db.Integer, db.ForeignKey('friendlist.id') ,nullable=False)
    users_send = db.Column(db.String(50), nullable=False)
    users_receiver = db.Column(db.String(50),nullable=False)
    message  = db.Column(db.String(1048), nullable=False)
    see_flag  = db.Column(db.String(4), nullable=False)
