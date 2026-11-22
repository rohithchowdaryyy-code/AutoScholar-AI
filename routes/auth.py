from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db
from models.student import Student

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.")
            return redirect(url_for("auth.register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect(url_for("auth.register"))

        existing_student = Student.query.filter_by(email=email).first()

        if existing_student:
            flash("This email is already registered.")
            return redirect(url_for("auth.register"))

        student = Student(
            name=name,
            email=email
        )

        student.set_password(password)

        try:
            db.session.add(student)
            db.session.commit()

            flash("Registration successful! Please log in.")
            return redirect(url_for("auth.login"))

        except Exception:
            db.session.rollback()
            flash("Registration failed. Please try again.")

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        student = Student.query.filter_by(email=email).first()

        if student and student.check_password(password):

            session["student_id"] = student.id
            session["student_name"] = student.name

            flash("Welcome back, " + student.name + "!")
            return redirect(url_for("home"))

        flash("Invalid email or password.")

    return render_template("login.html")


@auth.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.")
    return redirect(url_for("home"))
