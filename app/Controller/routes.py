from flask import render_template, flash, redirect, url_for, request,Blueprint
from app import  db
from flask_login import  current_user, login_required
from app.Controller.forms import ClassForm, EditForm
from app.Model.models import Class
from config import Config

routes_blueprint = Blueprint('routes',__name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER



@routes_blueprint.route("/", methods=["GET"])
@routes_blueprint.route("/index", methods=["GET"])
@login_required
def index():
    classes = Class.query.order_by(Class.major).all()
    return render_template(
        "index.html", title="Course List", classes=classes,
    )


@login_required
@routes_blueprint.route("/createclass/", methods=["GET", "POST"])
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
        return redirect(url_for("routes.index"))
    return render_template("create_class.html", form=cform)








@routes_blueprint.route("/display_profile/", methods=["GET"])
@login_required
def display_profile():
    return render_template(
        "display_profile.html",
        title="Display Profile",
        student=current_user,
    )


@routes_blueprint.route("/edit_profile/", methods=["GET", "POST"])
@login_required
def edit_profile():
    eform = EditForm()
    if request.method == "POST":
        # handle
        if eform.validate_on_submit:
            current_user.firstname = eform.firstname.data
            current_user.lastname = eform.lastname.data
            current_user.address = eform.address.data
            current_user.email = eform.email.data
            current_user.set_password(eform.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash("Changes saved")
            return redirect(url_for("routes.display_profile"))
            pass
    elif request.method == "GET":
        # pop
        eform.firstname.data = current_user.firstname
        eform.lastname.data = current_user.lastname
        eform.address.data = current_user.address
        eform.email.data = current_user.email
        pass
    else:
        pass
    return render_template("edit_profile.html", title="Edit Profile", form=eform)


@routes_blueprint.route("/roster/<classid>", methods=["GET"])
@login_required
def roster(classid):
    the_class = Class.query.filter_by(id=classid).first()
    return render_template("roster.html", title="roster", current_class=the_class)


@routes_blueprint.route("/enroll/<classid>", methods=["POST"])
@login_required
def enroll(classid):
    theClass = Class.query.filter_by(id=classid).first()
    if theClass is None:
        flash("class does not exist")
        return redirect(url_for("routes.index"))

    current_user.enroll(theClass)
    db.session.commit()
    flash("now Enrolled in {}".format(theClass.title))
    return redirect(url_for("routes.index"))


@routes_blueprint.route("/unenroll/<classid>", methods=["POST"])
@login_required
def unenroll(classid):
    theClass = Class.query.filter_by(id=classid).first()
    if theClass is None:
        flash("class does not exist")
        return redirect(url_for("routes.index"))
    current_user.unenroll(theClass)
    db.session.commit()
    flash("now unEnrolled in {}".format(theClass.title))
    return redirect(url_for("routes.index"))
