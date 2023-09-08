from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return Student.query.get(int(id))




class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenum = db.Column(db.String(3))
    title = db.Column(db.String(150))
    major = db.Column(db.String(20), db.ForeignKey("major.name"))
    roster = db.relationship('Enrolled',back_populates = "classenrolled")

    def __repr__(self):
        return "<Class id: {} - coursenum: {}>".format(self.id, self.coursenum)

    def getTitle(self):
        return self.title


class Major(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    department = db.Column(db.String(150))
    classes = db.relationship("Class", backref="coursemajor", lazy="dynamic")

    def __repr__(self):
        return "<Major - name: { } - department {}>".format(self.name, self.department)


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    address = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True, index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    classes = db.relationship('Enrolled',back_populates = 'studentenrolled')
 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def enroll(self,newclass):
        if not self.is_enrolled(newclass):
            newEnrollment = Enrolled(classenrolled = newclass)   
            self.classes.append(newEnrollment)
            db.session.commit()
    
    def unenroll(self, newclass):
     if self.is_enrolled(newclass):
        curEnrollment = Enrolled.query.filter_by(studentid=self.id).filter_by(classid = newclass.id).first()
        db.session.delete(curEnrollment)
        db.session.commit()

    def is_enrolled(self, newclass):
        if isinstance(newclass, int):
        
            return Enrolled.query.filter_by(studentid=self.id, classid=newclass).count() > 0
        elif isinstance(newclass, Class):
            
            return Enrolled.query.filter_by(studentid=self.id, classid=newclass.id).count() > 0
        else:
            return False


    def enrolledCourses(self):
        return self.classes
    

    def getEnrollmentDate(self,theclass):
        if self.is_enrolled(theclass):
            return Enrolled.query.filter_by(studentid = self.id).filter_by(classid=theclass.id).first().enrolldate
        else:
            return None



class Enrolled(db.Model):
    studentid = db.Column(db.Integer,db.ForeignKey('student.id'), primary_key=True)
    classid = db.Column(db.Integer,db.ForeignKey('class.id'), primary_key=True)
    enrolldate = db.Column(db.DateTime, default = datetime.utcnow())
    studentenrolled = db.relationship('Student')
    classenrolled = db.relationship('Class')
 