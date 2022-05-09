from . import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True)
    image_file = db.Column(db.String(100), default='default.jpg')
    password = db.Column(db.String(255))
    pitches = db.relationship('Pitch', backref='author', lazy="dynamic")
    comments = db.relationship('Comment', backref='user', lazy="dynamic")

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"User ('{self.username}','{self.email}','{self.image_file}')"
    
    
class Pitch(db.Model):
    __tablename__ = 'pitches'
    
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(50))
    content = db.Column(db.String(300))
    category_id = db.Column(db.String)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref='pitch', lazy="dynamic")


    def save_pitch(self, pitch):
        ''' Save the pitches '''
        db.session.add(pitch)
        db.session.commit()    
        
    def __repr__(self):
        return f"Pitch('{self.title}','{self.date_posted}')"
    
    
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment =db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    
    def save_comment(self, comment):
        ''' Save the commentss '''
        db.session.add(comment)
        db.session.commit()    
        
    def __repr__(self):
        return f"Comment('{self.comment}')"
    
