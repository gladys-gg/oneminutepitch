from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
import os



app = Flask(__name__)
app.config['SECRET_KEY']=os.environ.get['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///pitches.db'
#email configurations
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME ']= os.environ.get["MAIL_USERNAME"]
app.config['MAIL_PASSWORD ']= os.environ.get["MAIL_PASSWORD"]

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail= Mail(app)


login_manager = LoginManager(app)
login_manager.login_view = 'signIn'
login_manager.login_message_category ='info'







    




from app import views
