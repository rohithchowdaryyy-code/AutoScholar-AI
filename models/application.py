from datetime import datetime
from database import db


class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    scholarship_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarship.id"),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending",
        nullable=False
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    remarks = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "scholarship_id",
            name="unique_student_scholarship"
        ),
    )

    student = db.relationship(
        "Student",
        backref="applications"
    )

    scholarship = db.relationship(
        "Scholarship",
        backref="applications"
    )
