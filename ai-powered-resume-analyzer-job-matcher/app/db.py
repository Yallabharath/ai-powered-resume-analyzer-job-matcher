from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)
    entities = db.Column(db.Text)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def get_all_jobs():
    return Job.query.all()

def add_resume(filename, text, entities):
    resume = Resume(filename=filename, text=text, entities=str(entities))
    db.session.add(resume)
    db.session.commit()
