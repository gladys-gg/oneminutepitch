from flask import Flask, render_template,redirect,flash,url_for,request
from app import app,db
from app.models import User, Pitch
from .forms import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')