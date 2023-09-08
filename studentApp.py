from app import create_app, db
from app.Model.models import Major
from flask_login import current_user
from datetime import datetime
from config import Config
app = create_app(Config)
@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()
        if Major.query.count() == 0:
            majors = [{'name':'CptS','department':'School of EECS'},{'name':'SE','department':'Schoolof EECS'},{'name':'EE','department':'School of EECS'},
                    {'name':'ME','department':'Mechanical Engineering'}, {'name':'MATH','department': 'Mathematics'}  ]
            for t in majors:
                db.session.add(Major(name=t['name'],department=t['department']))
            db.session.commit()

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()




if __name__ == "__main__":
    app.run(debug=True)