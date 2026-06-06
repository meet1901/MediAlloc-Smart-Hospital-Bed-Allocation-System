from flask import Blueprint, render_template
from models import Bed

departments_bp = Blueprint("departments", __name__)


@departments_bp.route("/")
def dashboard():
    nephrology = Bed.query.filter_by(department_id=1, status="occupied").count()
    neurology = Bed.query.filter_by(department_id=2, status="occupied").count()
    cardiology = Bed.query.filter_by(department_id=3, status="occupied").count()

    return render_template(
        "index.html",
        nephrology_count=nephrology,
        neurology_count=neurology,
        cardiology_count=cardiology
    )