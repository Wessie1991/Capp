from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import and_

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

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
    chats = db.relationship('Chats', backref='Friendlist', lazy=True)

    def new_message(self, users_send, users_receiver, message):
        newmessage = Chats(id_Friendlist = self.id, users_send = users_send,
                           users_receiver = users_receiver, message=message)
        db.session.add(newmessage)
        db.session.commit()

class Chats(db.Model):
    __tableName__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    id_Friendlist =  db.Column(db.Integer, db.ForeignKey('friendlist.id') ,nullable=False)
    users_send = db.Column(db.String(50), nullable=False)
    users_receiver = db.Column(db.String(50),nullable=False)
    message  = db.Column(db.String(1048), nullable=False)
