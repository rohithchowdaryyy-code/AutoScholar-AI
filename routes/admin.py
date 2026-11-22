
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db
from models.admin import Admin
from models.student import Student
from models.scholarship import Scholarship
from models.application import Application
from datetime import datetime

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        admin = Admin.query.filter_by(email=email).first()

        if admin and admin.check_password(password):

            session.clear()
            session["admin_id"] = admin.id
            session["admin_name"] = admin.name

            flash("Welcome to Admin Dashboard!")
            return redirect(url_for("admin.dashboard"))

        flash("Invalid admin email or password.")

    return render_template("admin_login.html")


@admin_bp.route("/logout")
def logout():

    session.pop("admin_id", None)
    session.pop("admin_name", None)

    flash("Admin logged out successfully.")
    return redirect(url_for("admin.login"))


@admin_bp.route("/dashboard")
def dashboard():

    if "admin_id" not in session:
        flash("Please log in as admin.")
        return redirect(url_for("admin.login"))

    applications = Application.query.order_by(
        Application.applied_at.desc()
    ).all()

    total_students = Student.query.count()
    total_applications = Application.query.count()
    total_scholarships = Scholarship.query.filter_by(
        is_active=True
    ).count()

    return render_template(
        "admin_dashboard.html",
        admin_name=session.get("admin_name"),
        applications=applications,
        total_students=total_students,
        total_applications=total_applications,
        total_scholarships=total_scholarships
    )


@admin_bp.route(
    "/applications/<int:application_id>/status",
    methods=["POST"]
)
def update_application_status(application_id):

    if "admin_id" not in session:
        flash("Admin login required.")
        return redirect(url_for("admin.login"))

    application = db.session.get(Application, application_id)

    if not application:
        flash("Application not found.")
        return redirect(url_for("admin.dashboard"))

    new_status = request.form.get("status", "").strip()

    if new_status not in ["Approved", "Rejected"]:
        flash("Invalid application status.")
        return redirect(url_for("admin.dashboard"))

    application.status = new_status

    try:
        db.session.commit()
        flash(f"Application successfully marked as {new_status}!")

    except Exception:
        db.session.rollback()
        flash("Unable to update application status.")

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/students")
def students():

    if "admin_id" not in session:
        flash("Please log in as admin.")
        return redirect(url_for("admin.login"))

    students = Student.query.order_by(Student.id.desc()).all()

    return render_template(
        "admin_students.html",
        students=students
    )


@admin_bp.route("/scholarships/add", methods=["GET", "POST"])
def add_scholarship():

    if "admin_id" not in session:
        flash("Please log in as admin.")
        return redirect(url_for("admin.login"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        provider = request.form.get("provider", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not provider:
            flash("Scholarship title and provider are required.")
            return render_template("add_scholarship.html")

        try:
            amount = float(request.form.get("amount") or 0)
            max_income = float(request.form.get("max_income") or 0)
            min_percentage = float(request.form.get("min_percentage") or 0)

            if not 0 <= min_percentage <= 100:
                raise ValueError("Invalid minimum percentage.")

            deadline_text = request.form.get("deadline", "").strip()

            deadline = datetime.strptime(
                deadline_text, "%Y-%m-%d"
            ).date() if deadline_text else None

            scholarship = Scholarship(
                title=title,
                provider=provider,
                description=description,
                amount=amount,
                deadline=deadline,
                education=request.form.get("education", "").strip() or None,
                course=request.form.get("course", "").strip() or None,
                category=request.form.get("category", "").strip() or None,
                max_income=max_income if max_income > 0 else None,
                min_percentage=min_percentage if min_percentage > 0 else None,
                state=request.form.get("state", "").strip() or None,
                gender=request.form.get("gender", "").strip() or None,
                application_url=request.form.get("application_url", "").strip() or None,
                is_active=True
            )

            db.session.add(scholarship)
            db.session.commit()

            flash("Scholarship added successfully!")
            return redirect(url_for("admin.dashboard"))

        except ValueError:
            db.session.rollback()
            flash("Please enter valid numbers, percentage and deadline.")

        except Exception:
            db.session.rollback()
            flash("Unable to add scholarship. Please try again.")

    return render_template("add_scholarship.html")


@admin_bp.route("/scholarships")
def manage_scholarships():

    if "admin_id" not in session:
        flash("Please log in as admin.")
        return redirect(url_for("admin.login"))

    scholarships = Scholarship.query.order_by(
        Scholarship.id.desc()
    ).all()

    return render_template(
        "admin_scholarships.html",
        scholarships=scholarships
    )


@admin_bp.route(
    "/scholarships/<int:scholarship_id>/toggle",
    methods=["POST"]
)
def toggle_scholarship(scholarship_id):

    if "admin_id" not in session:
        flash("Please log in as admin.")
        return redirect(url_for("admin.login"))

    scholarship = db.session.get(Scholarship, scholarship_id)

    if not scholarship:
        flash("Scholarship not found.")
        return redirect(url_for("admin.manage_scholarships"))

    scholarship.is_active = not scholarship.is_active

    try:
        db.session.commit()

        status = "activated" if scholarship.is_active else "deactivated"
        flash(f"Scholarship successfully {status}!")

    except Exception:
        db.session.rollback()
        flash("Unable to update scholarship status.")

    return redirect(url_for("admin.manage_scholarships"))


@admin_bp.route(
    "/scholarships/<int:scholarship_id>/edit",
    methods=["GET", "POST"]
)
def edit_scholarship(scholarship_id):

    if "admin_id" not in session:
        flash("Please log in as admin.")
        return redirect(url_for("admin.login"))

    scholarship = db.session.get(Scholarship, scholarship_id)

    if not scholarship:
        flash("Scholarship not found.")
        return redirect(url_for("admin.manage_scholarships"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        provider = request.form.get("provider", "").strip()

        if not title or not provider:
            flash("Title and provider are required.")
            return render_template(
                "edit_scholarship.html",
                scholarship=scholarship
            )

        try:
            scholarship.title = title
            scholarship.provider = provider
            scholarship.description = request.form.get("description", "").strip()

            scholarship.amount = float(
                request.form.get("amount") or 0
            )

            deadline_text = request.form.get("deadline", "").strip()

            scholarship.deadline = (
                datetime.strptime(deadline_text, "%Y-%m-%d").date()
                if deadline_text else None
            )

            scholarship.education = request.form.get("education", "").strip() or None
            scholarship.course = request.form.get("course", "").strip() or None
            scholarship.category = request.form.get("category", "").strip() or None

            income = float(request.form.get("max_income") or 0)
            scholarship.max_income = income if income > 0 else None

            percentage = float(request.form.get("min_percentage") or 0)

            if not 0 <= percentage <= 100:
                raise ValueError("Invalid minimum percentage.")

            scholarship.min_percentage = percentage if percentage > 0 else None

            scholarship.state = request.form.get("state", "").strip() or None
            scholarship.gender = request.form.get("gender", "").strip() or None
            scholarship.application_url = request.form.get("application_url", "").strip() or None

            db.session.commit()

            flash("Scholarship updated successfully!")
            return redirect(url_for("admin.manage_scholarships"))

        except ValueError:
            db.session.rollback()
            flash("Please enter valid numbers, percentage and deadline.")

        except Exception:
            db.session.rollback()
            flash("Unable to update scholarship.")

    return render_template(
        "edit_scholarship.html",
        scholarship=scholarship
    )
