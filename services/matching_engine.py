def check_eligibility(student, scholarship):

    reasons = []
    score = 0
    total_checks = 0

    # 1. Check Education
    if scholarship.education:
        total_checks += 1

        if student.education:
            if student.education.strip().lower() == scholarship.education.strip().lower():
                score += 1
            else:
                reasons.append("Education requirement not matched.")
        else:
            reasons.append("Please update your education details.")

    # 2. Check Course
    if scholarship.course:
        total_checks += 1

        if student.course:
            if student.course.strip().lower() == scholarship.course.strip().lower():
                score += 1
            else:
                reasons.append("Course requirement not matched.")
        else:
            reasons.append("Please update your course details.")

    # 3. Check Category
    if scholarship.category:
        total_checks += 1

        if student.category:
            student_category = student.category.strip().upper()
            scholarship_category = scholarship.category.strip().upper()

            if student_category == scholarship_category:
                score += 1

            elif scholarship_category == "SC/ST" and student_category in ["SC", "ST"]:
                score += 1

            else:
                reasons.append("Category requirement not matched.")
        else:
            reasons.append("Please update your category.")

    # 4. Check Annual Family Income
    if scholarship.max_income is not None:
        total_checks += 1

        if student.annual_income is not None:
            if student.annual_income <= scholarship.max_income:
                score += 1
            else:
                reasons.append("Annual income exceeds the scholarship limit.")
        else:
            reasons.append("Please update your annual family income.")

    # 5. Check Academic Percentage
    if scholarship.min_percentage is not None:
        total_checks += 1

        if student.percentage is not None:
            if student.percentage >= scholarship.min_percentage:
                score += 1
            else:
                reasons.append("Academic percentage is below the required minimum.")
        else:
            reasons.append("Please update your academic percentage.")

    # 6. Check State
    if scholarship.state:
        total_checks += 1

        if student.state:
            if student.state.strip().lower() == scholarship.state.strip().lower():
                score += 1
            else:
                reasons.append("State requirement not matched.")
        else:
            reasons.append("Please update your state.")

    # 7. Check Gender
    if scholarship.gender:
        total_checks += 1

        if student.gender:
            if student.gender.strip().lower() == scholarship.gender.strip().lower():
                score += 1
            else:
                reasons.append("Gender requirement not matched.")
        else:
            reasons.append("Please update your gender.")

    # Handle scholarships without eligibility requirements
    if total_checks == 0:
        return {
            "eligible": None,
            "score": 0,
            "reasons": ["Eligibility requirements are not specified."]
        }

    # Calculate matching percentage
    percentage = round((score / total_checks) * 100)

    return {
        "eligible": score == total_checks,
        "score": percentage,
        "reasons": reasons
    }