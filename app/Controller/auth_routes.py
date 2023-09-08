from flask import render_template, flash, redirect, url_for, request,Blueprint
from app import  db
from flask_login import login_user, current_user, logout_user, login_required

from app.Controller.forms import  EditForm, EmptyForm
from app.Controller.auth_forms import RegistrationForm, LoginForm
from app.Model.models import  Student
from config import Config

routes_blueprint = Blueprint('auth',__name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER

@routes_blueprint.route("/register/", methods=["GET", "POST"])
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
        flash("congrats your signed up")
        return redirect(url_for("routes.index"))
    return render_template("register.html", form=rform)

@routes_blueprint.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))

    lform = LoginForm()
    if lform.validate_on_submit():
        student = Student.query.filter_by(username=lform.username.data).first()
        if (student is None) or (student.check_password(lform.password.data) == False):
            flash("invaild username or password")
            return redirect(url_for("auth.login"))
        login_user(student, lform.remember_me.data)
        return redirect(url_for("routes.index"))
    return render_template("login.html", title="sign in", form=lform)


@routes_blueprint.route("/logout/", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))