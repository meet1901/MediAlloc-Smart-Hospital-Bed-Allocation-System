from flask import Flask
from config import Config
from models import db, Department, Bed
from routes.patients import patients_bp
from routes.beds import beds_bp
from routes.departments import departments_bp
from routes.allocations import allocations_bp

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.register_blueprint(patients_bp)
app.register_blueprint(beds_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(allocations_bp)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

    # Add departments if not already added
    if Department.query.count() == 0:
        db.session.add_all([
            Department(name="Nephrology"),
            Department(name="Neurology"),
            Department(name="Cardiology")
        ])
        db.session.commit()

    # Add 15 beds for each department if not already added
    if Bed.query.count() == 0:
        for dept_id in [1, 2, 3]:
            for i in range(1, 16):
                db.session.add(Bed(department_id=dept_id, bed_number=i, status="empty"))
        db.session.commit()

@app.route("/")
def home():
    return "Database setup successful! Next step: routes + frontend"

if __name__ == "__main__":
    app.run(debug=True)