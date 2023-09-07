from app import db
from flask import Flask
#create the database file, if it doesn't exist. 
db.create_all

# import db models
from app.models import Class,Major,enrolled,Student

#create class objects and write them to the database
newClass = Class(coursenum='322')
db.session.add(newClass)
newClass = Class(coursenum='355')
db.session.add(newClass)
db.session.commit()

c1 = Class.query.filter_by(coursenum='322').first()
s1 = Student.query.filter_by(username='kyan').first()

s1.classes.append(c1)
db.session.commit()
newMajor = Major(name = "Cpts", department = "Voiland College of Engineering")
db.session.add(newMajor)
db.session.commit()
# query and print classes
Class.query.all()
Class.query.filter_by(coursenum='322').all()
Class.query.filter_by(coursenum='322').first()
myclasses = Class.query.order_by(Class.coursenum.desc()).all()
for c in myclasses:
    print(c.coursenum)
