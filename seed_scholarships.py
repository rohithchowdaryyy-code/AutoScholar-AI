from datetime import date, timedelta

from app import app
from database import db
from models.scholarship import Scholarship


demo_scholarships = [
    {
        "title": "Merit Excellence Scholarship",
        "provider": "AutoScholar Demo Foundation",
        "description": "Demo scholarship for students with strong academic performance.",
        "amount": 25000,
        "education": "BTech",
        "course": "AIML",
        "category": None,
        "max_income": 500000
    },
    {
        "title": "Engineering Student Support",
        "provider": "AutoScholar Demo Foundation",
        "description": "Illustrative financial support for engineering students.",
        "amount": 20000,
        "education": "BTech",
        "course": None,
        "category": None,
        "max_income": 300000
    },
    {
        "title": "Women in Technology Scholarship",
        "provider": "AutoScholar Demo Foundation",
        "description": "Demo scholarship record for women pursuing technology education.",
        "amount": 30000,
        "education": "BTech",
        "course": None,
        "category": None,
        "max_income": 400000
    },
    {
        "title": "SC/ST Education Support",
        "provider": "AutoScholar Demo Foundation",
        "description": "Illustrative scholarship record for SC/ST category students.",
        "amount": 15000,
        "education": "BTech",
        "course": None,
        "category": "SC/ST",
        "max_income": 300000
    },
    {
        "title": "Need Based Student Scholarship",
        "provider": "AutoScholar Demo Foundation",
        "description": "Demo financial assistance for students from lower-income families.",
        "amount": 10000,
        "education": None,
        "course": None,
        "category": None,
        "max_income": 200000
    }
]


with app.app_context():

    added = 0

    for item in demo_scholarships:

        existing = Scholarship.query.filter_by(
            title=item["title"]
        ).first()

        if existing:
            continue

        scholarship = Scholarship(
            **item,
            deadline=date.today() + timedelta(days=60),
            is_active=True
        )

        db.session.add(scholarship)
        added += 1

    db.session.commit()

    print(f"Successfully added {added} demo scholarships!")

    print(
        "Total scholarships:",
        Scholarship.query.filter_by(is_active=True).count()
    )