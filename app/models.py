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
    title =  db.Column(db.String(150))  
    major = db.Column(db.String(20),db.ForeignKey("major.name"))

    def __repr__(self):
        return '<Class id: {} - coursenum: {}>'.format(self.id,self.coursenum)
    def getTitle(self):
        return self.title
    
class Major(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    department = db.Column(db.String(150))
    classes = db.relationship('Class',backref='coursemajor',lazy='dynamic')
    def __repr__(self):
        return'<Major - name: { } - department {}>'.format(self.name,self.department)


class Student(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique = True, index = True)    
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    address = db.Column(db.String(128))
    email = db.Column(db.String(128), unique = True, index = True)
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
   
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)