from flask import render_template, flash, redirect, url_for, request
from app import app, db

from app.forms import ClassForm, RegistrationForm
from app.models import Class, Major, Student


@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    classes = Class.query.order_by(Class.major).all()
    return render_template("index.html", title="Course List", classes=classes)


@app.route("/createclass/", methods=["GET", "POST"])
def createclass():
    cform = ClassForm()
    if cform.validate_on_submit():
        newClass = Class(
            coursenum=cform.coursenum.data,
            title=cform.title.data,
            major=cform.major.data.name,
        )
        db.session.add(newClass)
        db.session.commit()
        flash(
            'Class "'
            + newClass.major
            + " "
            + newClass.coursenum
            + " "
            + newClass.title
            + '"'
        )
        return redirect(url_for("index"))
    return render_template("create_class.html", form=cform)


@app.route("/register/", methods=["GET", "POST"])
def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():
        student = Student(
            username=rform.username.data,
            email=rform.email.data,
            firstname=rform.firstname.data,
            lastname=rform.lastname.data,
            address=rform.address.data,
        )
        student.set_password(rform.password.data)
        db.session.add(student)
        db.session.commit()
        flash('congrats your signed up')
        return redirect(url_for("index"))
    return render_template("register.html", form=rform)
