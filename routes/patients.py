from flask import Blueprint, render_template, request, redirect, flash
from models import db, Patient, Department, Bed, WaitingList, Allocation

patients_bp = Blueprint("patients", __name__)

priority_order = {
    "Extreme": 1,
    "High": 2,
    "Moderate": 3,
    "Normal": 4
}


@patients_bp.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    departments = Department.query.all()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        disease = request.form["disease"]
        dept_id = int(request.form["required_department"])
        severity = request.form["priority"]

        patient = Patient(
            name=name,
            age=age,
            disease=disease,
            severity=severity,
            required_department_id=dept_id
        )

        db.session.add(patient)
        db.session.commit()

        # =========================
        # STEP 1: Try empty bed
        # =========================
        bed = Bed.query.filter_by(department_id=dept_id, status="empty").first()

        if bed:
            bed.status = "occupied"
            patient.assigned_department_id = dept_id

            alloc = Allocation(patient_id=patient.id, bed_id=bed.id)
            db.session.add(alloc)
            db.session.commit()

            flash("Patient admitted successfully!", "success")
            return redirect("/patients")

        # =========================
        # STEP 2: PRIORITY REPLACEMENT
        # =========================
        allocations = Allocation.query.filter_by(discharged_at=None).all()

        dept_allocs = []
        for alloc in allocations:
            bed_obj = Bed.query.get(alloc.bed_id)
            if bed_obj.department_id == dept_id:
                dept_allocs.append(alloc)

        lowest_alloc = None
        lowest_priority = -1

        for alloc in dept_allocs:
            p = alloc.patient
            p_priority = priority_order[p.severity]

            if p_priority > lowest_priority:
                lowest_priority = p_priority
                lowest_alloc = alloc

        new_priority = priority_order[severity]

        if lowest_alloc and new_priority < lowest_priority:
            old_patient = lowest_alloc.patient
            old_bed = Bed.query.get(lowest_alloc.bed_id)

            # assign new patient
            patient.assigned_department_id = dept_id

            new_alloc = Allocation(patient_id=patient.id, bed_id=old_bed.id)
            db.session.add(new_alloc)

            # remove old allocation
            db.session.delete(lowest_alloc)

            # try shifting old patient
            other_depts = Department.query.filter(Department.id != dept_id).all()
            shifted = False

            for d in other_depts:
                free_bed = Bed.query.filter_by(department_id=d.id, status="empty").first()
                if free_bed:
                    free_bed.status = "occupied"
                    old_patient.assigned_department_id = d.id
                    old_patient.is_shifted = True

                    new_alloc2 = Allocation(patient_id=old_patient.id, bed_id=free_bed.id)
                    db.session.add(new_alloc2)

                    shifted = True
                    break

            if not shifted:
                old_patient.status = "waiting"
                wait = WaitingList(
                    patient_id=old_patient.id,
                    department_id=dept_id,
                    priority=old_patient.severity
                )
                db.session.add(wait)

            db.session.commit()

            flash("Higher priority patient replaced lower priority patient.", "warning")
            return redirect("/patients")

        # =========================
        # STEP 3: Try shifting new patient
        # =========================
        other_depts = Department.query.filter(Department.id != dept_id).all()

        for d in other_depts:
            free_bed = Bed.query.filter_by(department_id=d.id, status="empty").first()
            if free_bed:
                free_bed.status = "occupied"
                patient.assigned_department_id = d.id
                patient.is_shifted = True

                alloc = Allocation(patient_id=patient.id, bed_id=free_bed.id)
                db.session.add(alloc)
                db.session.commit()

                flash("Patient shifted to another department.", "info")
                return redirect("/patients")

        # =========================
        # STEP 4: WAITING LIST
        # =========================
        patient.status = "waiting"

        wait = WaitingList(
            patient_id=patient.id,
            department_id=dept_id,
            priority=severity
        )

        db.session.add(wait)
        db.session.commit()

        flash("No beds available anywhere. Added to waiting list.", "danger")
        return redirect("/waiting_list")

    return render_template("add_patient.html", departments=departments)


@patients_bp.route("/patients")
def view_patients():
    patients = Patient.query.all()
    return render_template("patients.html", patients=patients)


@patients_bp.route("/waiting_list")
def waiting_list():
    waiting = WaitingList.query.all()
    waiting = sorted(waiting, key=lambda x: priority_order[x.priority])

    return render_template("waiting_list.html", waiting_patients=waiting)