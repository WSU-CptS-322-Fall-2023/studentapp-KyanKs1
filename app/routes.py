from flask import render_template, flash, redirect, url_for, request
from app import app,db

from app.forms import ClassForm
from app.models import Class,Major

@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    classes = Class.query.order_by(Class.major).all()
    return render_template('index.html', title="Course List",classes=classes)