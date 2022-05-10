from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo,ValidationError
from app.models import *



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('Sign Up')
    
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. PLease choose a different one.')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. PLease choose a different one.')


class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
    
class NewPitchForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Pitch Category', choices=[('product', 'product'),
                                                      ('service', 'service'),
                                                      ('Pick Up Line', 'PickUpLine'),
                                                      ('business', 'business')])
    content =TextAreaField('New Pitch', validators=[DataRequired()])
    submit = SubmitField('Post')
    

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    
    bio =TextAreaField('About yourself', validators=[DataRequired()])
    
    submit = SubmitField('Update')
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. PLease choose a different one.')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. PLease choose a different one.')
            

class CommentForm(FlaskForm):

    title = StringField('Comment Title')
    comment = TextAreaField('Post Of The Comment')
    submit = SubmitField('Submit')
 