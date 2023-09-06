from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import  ValidationError, Length,DataRequired
from app.models import Class,Major


def get_major():
    return Major.query.all()

def get_majorlabel(theMajor):
    return theMajor.name


class ClassForm(FlaskForm):
    coursenum = StringField('Course Number',[Length(min=3, max=3)])
    title = StringField('Class Title', validators=[DataRequired()])
    major = QuerySelectField('Majors',query_factory = get_major, get_label= get_majorlabel, allow_blank=False )
    submit = SubmitField('Post')



