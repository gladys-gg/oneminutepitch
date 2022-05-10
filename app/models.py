from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True)
    image_file = db.Column(db.String(100), default='default.jpg')
    password = db.Column(db.String(255))
    pitches = db.relationship('Pitch', backref='author')
    comments = db.relationship('Comment', backref='author')
    likes = db.relationship('Like', backref='author' )

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    comments = db.relationship('Comment', backref='pitch')
    likes = db.relationship('Like', backref='pitch')


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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    pitches_id = db.Column(db.Integer, db.ForeignKey('pitches.id', ondelete="CASCADE"))
    
    def save_comment(self, comment):
        ''' Save the commentss '''
        db.session.add(comment)
        db.session.commit()    
        
    def __repr__(self):
        return f"Comment('{self.comment}')"
    
class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id', ondelete="CASCADE"))
    
    
