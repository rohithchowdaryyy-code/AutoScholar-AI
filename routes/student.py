
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from database import db
from models.student import Student
from models.scholarship import Scholarship
from models.application import Application

student_bp = Blueprint("student", __name__)


@student_bp.route("/dashboard")
def dashboard():

    # Check whether the student is logged in
    if "student_id" not in session:
        flash("Please log in to access your dashboard.")
        return redirect(url_for("auth.login"))

    # Get the logged-in student's details
    student = Student.query.get(session["student_id"])

    if not student:
        session.clear()
        flash("Student account not found. Please log in again.")
        return redirect(url_for("auth.login"))

    # Calculate dashboard statistics
    total_scholarships = Scholarship.query.filter_by(
        is_active=True
    ).count()

    total_applications = Application.query.filter_by(
        student_id=student.id
    ).count()

    pending_applications = Application.query.filter_by(
        student_id=student.id,
        status="Pending"
    ).count()

    # Get student's applications
    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    return render_template(
        "dashboard.html",
        student=student,
        total_scholarships=total_scholarships,
        total_applications=total_applications,
        pending_applications=pending_applications,
        applications=applications
    )


@student_bp.route("/profile", methods=["GET", "POST"])
def profile():

    # Check whether the student is logged in
    if "student_id" not in session:
        flash("Please log in to access your profile.")
        return redirect(url_for("auth.login"))

    # Get student details
    student = Student.query.get(session["student_id"])

    if not student:
        session.clear()
        flash("Student account not found. Please log in again.")
        return redirect(url_for("auth.login"))

    # Handle profile form submission
    if request.method == "POST":

        percentage = request.form.get("percentage", "").strip()
        annual_income = request.form.get("annual_income", "").strip()

        try:
            percentage_value = float(percentage) if percentage else None
            income_value = float(annual_income)

            if percentage_value is not None and not 0 <= percentage_value <= 100:
                raise ValueError

            if income_value < 0:
                raise ValueError

        except ValueError:
            flash("Please enter valid percentage (0-100) and annual income values.")
            return redirect(url_for("student.profile"))

        # Update student information
        student.education = request.form.get("education")
        student.course = request.form.get("course")
        student.category = request.form.get("category")
        student.state = request.form.get("state")
        student.gender = request.form.get("gender")
        student.percentage = percentage_value
        student.annual_income = income_value

        # Save changes to database
        db.session.commit()

        flash("Your profile has been updated successfully!")
        return redirect(url_for("student.profile"))

    # Display profile page
    return render_template("profile.html", student=student)
