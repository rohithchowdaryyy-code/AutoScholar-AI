from models.scholarship import Scholarship


def get_all_scholarships():
    return Scholarship.query.filter_by(
        is_active=True
    ).all()


def search_scholarships(keyword):

    return Scholarship.query.filter(
        Scholarship.is_active == True,
        (
            Scholarship.title.ilike(f"%{keyword}%") |
            Scholarship.provider.ilike(f"%{keyword}%")
        )
    ).all()


def get_scholarship_by_id(scholarship_id):

    return Scholarship.query.filter_by(
        id=scholarship_id,
        is_active=True
    ).first()