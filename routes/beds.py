from flask import Blueprint, render_template
from models import Department, Allocation

beds_bp = Blueprint("beds", __name__)

@beds_bp.route("/beds")
def view_beds():
    departments = Department.query.all()

    # Get active allocations
    allocations = Allocation.query.filter_by(discharged_at=None).all()

    # Map bed_id → patient
    bed_patient_map = {alloc.bed_id: alloc.patient for alloc in allocations}

    return render_template(
        "beds.html",
        departments=departments,
        bed_patient_map=bed_patient_map
    )