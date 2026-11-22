from database import db


class Scholarship(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    provider = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    amount = db.Column(db.Float)

    deadline = db.Column(db.Date)

    education = db.Column(db.String(100))

    course = db.Column(db.String(100))

    category = db.Column(db.String(50))

    max_income = db.Column(db.Float)

    min_percentage = db.Column(db.Float)

    state = db.Column(db.String(100))
    
    gender = db.Column(db.String(30))

    application_url = db.Column(db.String(500))

    is_active = db.Column(db.Boolean, default=True)
