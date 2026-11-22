from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.student import Student
from models.scholarship import Scholarship
from services.matching_engine import check_eligibility

scholarship_bp = Blueprint("scholarship", __name__)


@scholarship_bp.route("/scholarships")
def scholarship_list():

    if "student_id" not in session:
        flash("Please log in to view scholarships.")
        return redirect(url_for("auth.login"))

    student = Student.query.get(session["student_id"])

    if not student:
        session.clear()
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "").strip()

    query = Scholarship.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            Scholarship.title.ilike(f"%{search}%") |
            Scholarship.provider.ilike(f"%{search}%") |
            Scholarship.description.ilike(f"%{search}%")
        )

    scholarships = query.order_by(Scholarship.deadline.asc()).all()

    eligibility_results = {
        scholarship.id: check_eligibility(student, scholarship)
        for scholarship in scholarships
    }

    return render_template(
        "scholarship.html",
        scholarships=scholarships,
        search=search,
        eligibility_results=eligibility_results
    )