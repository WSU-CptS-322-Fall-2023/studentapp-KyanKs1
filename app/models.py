from app import db

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


