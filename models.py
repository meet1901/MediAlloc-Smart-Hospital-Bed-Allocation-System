from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Bed(db.Model):
    __tablename__ = "beds"

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    bed_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="empty")

    department = db.relationship("Department", backref="beds")


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    disease = db.Column(db.String(255))
    severity = db.Column(db.String(20), nullable=False)

    required_department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    assigned_department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)

    is_shifted = db.Column(db.Boolean, default=False)
    admitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="active")

    required_department = db.relationship("Department", foreign_keys=[required_department_id])
    assigned_department = db.relationship("Department", foreign_keys=[assigned_department_id])


class WaitingList(db.Model):
    __tablename__ = "waiting_list"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    queue_time = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", backref="waiting_entries")
    department = db.relationship("Department", backref="waiting_patients")


class Allocation(db.Model):
    __tablename__ = "allocations"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    bed_id = db.Column(db.Integer, db.ForeignKey("beds.id"), nullable=False)
    allocated_at = db.Column(db.DateTime, default=datetime.utcnow)
    discharged_at = db.Column(db.DateTime, nullable=True)

    patient = db.relationship("Patient", backref="allocations")
    bed = db.relationship("Bed", backref="allocations")