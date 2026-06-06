from flask import Blueprint, redirect
from models import db, Patient, Bed, Allocation, WaitingList

allocations_bp = Blueprint("allocations", __name__)

priority_order = {
    "Extreme": 1,
    "High": 2,
    "Moderate": 3,
    "Normal": 4
}


@allocations_bp.route("/discharge/<int:id>")
def discharge(id):
    patient = Patient.query.get(id)

    allocation = Allocation.query.filter_by(patient_id=id, discharged_at=None).first()

    if allocation:
        bed = Bed.query.get(allocation.bed_id)
        bed.status = "empty"
        allocation.discharged_at = db.func.now()
        patient.status = "discharged"

        db.session.commit()

        # Assign highest-priority waiting patient
        waiting = WaitingList.query.filter_by(department_id=bed.department_id).all()

        if waiting:
            waiting = sorted(waiting, key=lambda x: priority_order[x.priority])
            next_wait = waiting[0]

            next_patient = Patient.query.get(next_wait.patient_id)

            bed.status = "occupied"
            next_patient.status = "active"
            next_patient.assigned_department_id = bed.department_id

            new_alloc = Allocation(patient_id=next_patient.id, bed_id=bed.id)

            db.session.add(new_alloc)
            db.session.delete(next_wait)
            db.session.commit()

    return redirect("/patients")