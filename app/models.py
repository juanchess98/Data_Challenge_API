from app import db
# Create table entities

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    datetime = db.Column(db.String(128), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('Jobs.id'), nullable=False)

class Department(db.Model):
    __tablename__ = 'Departments'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(64), nullable=False)
    employees = db.relationship('Employee', backref='department', lazy=True)

class Job(db.Model):
    __tablename__ = 'Jobs'
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(64), nullable=False)
    employees = db.relationship('Employee', backref='job', lazy=True)