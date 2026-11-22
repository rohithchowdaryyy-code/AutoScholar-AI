from flask import Blueprint, render_template, request, session, jsonify
from models.student import Student
from models.scholarship import Scholarship
from models.application import Application
from services.matching_engine import check_eligibility
from datetime import date

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chatbot")
def chatbot():

    if "student_id" not in session:
        return "Please log in first.", 401

    return render_template("chatbot.html")


@chatbot_bp.route("/chatbot/ask", methods=["POST"])
def ask():

    if "student_id" not in session:
        return jsonify({"reply": "Please log in first."}), 401

    student = Student.query.get(session["student_id"])

    if not student:
        return jsonify({"reply": "Student account not found."}), 404

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip().lower()

    if not message:
        return jsonify({"reply": "Please enter a question."})

          # Understand the student's question

    if any(word in message for word in [
        "application", "status", "approved",
        "rejected", "pending", "accepted"
    ]):
        intent = "application"

    elif any(word in message for word in [
        "document", "certificate", "marksheet",
        "proof", "submit", "paperwork"
    ]):
        intent = "documents"

    elif any(word in message for word in [
        "deadline", "expire", "last date",
        "when should i apply", "closing date"
    ]):
        intent = "deadline"

    elif any(word in message for word in [
        "details", "amount", "provider",
        "application link", "website",
        "scholarship information"
     ]):
        intent = "details"

    elif any(word in message for word in [
        "eligible", "eligibility", "recommend",
        "suitable", "scholarship", "scholarships",
        "financial aid", "financial assistance",
        "apply for"
    ]):
        intent = "eligibility"

    else:
        intent = "general"

    if intent == "eligibility":

        scholarships = Scholarship.query.filter_by(is_active=True).all()

        recommendations = []

        for scholarship in scholarships:

            result = check_eligibility(student, scholarship)

            recommendations.append({
                "title": scholarship.title,
                "score": result["score"],
                "eligible": result["eligible"],
                "reasons": result["reasons"],
                "amount": scholarship.amount,
                "deadline": scholarship.deadline
            })

        # Rank by match score, highest first
        recommendations.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        reply = "🏆 Your Smart Scholarship Recommendations\n\n"

        if recommendations:

            for item in recommendations:

                status = (
                    "✅ Matches checked requirements"
                    if item["eligible"] is True
                    else "⚠️ Partial match"
                    if item["eligible"] is False
                    else "ℹ️ Requirements not specified"
                )

                reply += (
                    f"🎓 {item['title']}\n"
                    f"Match Score: {item['score']}%\n"
                    f"Status: {status}\n"
                    f"Award: ₹{item['amount'] or 0:,.0f}\n"
                    f"Deadline: {item['deadline'] or 'Not specified'}\n"
                )

                if item["reasons"]:
                    reply += "Reasons:\n"
                    reply += "\n".join(
                        "• " + reason
                        for reason in item["reasons"]
                    )
                    reply += "\n"

                reply += "\n"

        else:
            reply += "No active scholarships are currently available."
    elif intent == "details":

        scholarships = Scholarship.query.filter_by(is_active=True).all()

        reply = "🎓 Available Scholarship Details\n\n"

        for scholarship in scholarships:

            reply += f"📌 {scholarship.title}\n"
            reply += f"Provider: {scholarship.provider}\n"
            reply += f"Award Amount: ₹{scholarship.amount or 0:,.0f}\n"
            reply += f"Deadline: {scholarship.deadline or 'Not specified'}\n"
            reply += f"Application Link: {scholarship.application_url or 'Not available'}\n\n"

        if not scholarships:
            reply = "No active scholarships are currently available."
    elif intent == "documents":

        reply = (
            "Common scholarship documents may include:\n"
            "• Aadhaar or other accepted identity proof\n"
            "• Income certificate\n"
            "• Previous academic marksheets\n"
            "• College ID or bonafide certificate\n"
            "• Bank account details\n\n"
            "Requirements vary by scholarship. Always verify them with the official provider."
        )

    
    elif intent == "deadline":

        scholarships = Scholarship.query.filter_by(is_active=True).all()

        today = date.today()

        upcoming = []
        expired = []
        no_deadline = []

        for scholarship in scholarships:

            if scholarship.deadline is None:
                no_deadline.append(scholarship.title)

            elif scholarship.deadline >= today:
                upcoming.append(
                    f"{scholarship.title}: {scholarship.deadline}"
                )

            else:
                expired.append(
                    f"{scholarship.title}: {scholarship.deadline}"
                )

        reply = "📅 Scholarship Deadline Report\n\n"

        reply += "🟢 Upcoming Deadlines:\n"

        if upcoming:
            reply += "\n".join("• " + item for item in upcoming)
        else:
            reply += "No upcoming deadlines."

        reply += "\n\n🔴 Expired Deadlines:\n"

        if expired:
            reply += "\n".join("• " + item for item in expired)
        else:
            reply += "No expired deadlines."

        reply += "\n\n⚪ Scholarships Without Deadlines:\n"

        if no_deadline:
            reply += "\n".join("• " + item for item in no_deadline)
        else:
            reply += "None." 

    else:
        reply = (
            "Hello! I'm your AutoScholar Assistant. 🤖\n\n"
            "You can ask me:\n"
            "• Which scholarships am I eligible for?\n"
            "• What is my application status?\n"
            "• What documents do I need?\n"
            "• What are the scholarship deadlines?"
        )

    return jsonify({"reply": reply})