from getpass import getpass

from app import app
from database import db
from models.admin import Admin


with app.app_context():

    print("===== AutoScholar AI Admin Setup =====")

    name = input("Enter admin name: ").strip()
    email = input("Enter admin email: ").strip().lower()
    password = getpass("Create admin password: ")
    confirm_password = getpass("Confirm admin password: ")

    if not name or not email or not password:
        print("All fields are required.")

    elif len(password) < 12:
        print("Password must contain at least 12 characters.")

    elif password != confirm_password:
        print("Passwords do not match.")

    elif Admin.query.filter_by(email=email).first():
        print("An admin with this email already exists.")

    else:
        admin = Admin(name=name, email=email)
        admin.set_password(password)

        try:
            db.session.add(admin)
            db.session.commit()
            print("Admin account created successfully!")

        except Exception:
            db.session.rollback()
            print("Admin creation failed.")