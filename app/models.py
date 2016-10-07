#coding: utf-8

from app.model_base import db, login_manager
from flask_login import UserMixin


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    users = db.relationship('User', backref='role')

    @staticmethod
    def seed():
        db.session.add_all(map(lambda r: Role(name=r), ['Guests', 'Administrators']))
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @staticmethod
    def on_created(target, value, oldvalue, initiator):
        target.role = Role.query.filter_by(name='Guests').first()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.event.listen(User.name, 'set', User.on_created)
