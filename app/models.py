from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True)
    password = db.Column(db.String(255))
    # pitches = db.relationship('Pitch', backref='author', lazy="dynamic")
    # comments = db.relationship('Comment', backref='user', lazy="dynamic")

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'
