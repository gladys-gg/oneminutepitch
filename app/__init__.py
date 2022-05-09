from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY']='hithere123'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///pitches.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


return app