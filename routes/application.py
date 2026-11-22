from flask import Blueprint, session, redirect, url_for, flash
from database import db
from models.application import Application
from models.scholarship import Scholarship
from models.student import Student
from services.matching_engine import check_eligibility

application_bp = Blueprint("application", __name__)


@application_bp.route("/apply/<int:scholarship_id>", methods=["POST"])
def apply(scholarship_id):

    if "student_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("auth.login"))

    student = db.session.get(Student, session["student_id"])

    if not student:
        session.clear()
        flash("Please log in again.")
        return redirect(url_for("auth.login"))

    scholarship = db.session.get(Scholarship, scholarship_id)

    if not scholarship or not scholarship.is_active:
        flash("Scholarship not found.")
        return redirect(url_for("scholarship.scholarship_list"))

    existing = Application.query.filter_by(
        student_id=student.id,
        scholarship_id=scholarship.id
    ).first()

    if existing:
        flash("You have already applied for this scholarship.")
        return redirect(url_for("scholarship.scholarship_list"))

    result = check_eligibility(student, scholarship)

    if result["eligible"] is not True:
        flash("You are not currently eligible. Complete your profile and check the requirements.")
        return redirect(url_for("scholarship.scholarship_list"))

    application = Application(
        student_id=student.id,
        scholarship_id=scholarship.id,
        status="Pending"
    )

    try:
        db.session.add(application)
        db.session.commit()
        flash("Application submitted successfully!")

    except Exception:
        db.session.rollback()
        flash("Application submission failed. Please try again.")

    return redirect(url_for("student.dashboard"))