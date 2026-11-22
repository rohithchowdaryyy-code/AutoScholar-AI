from flask import Flask, render_template
from config import Config
from database import db


def create_app():

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Register authentication routes
    from routes.auth import auth
    app.register_blueprint(auth)

    # Register student dashboard routes
    from routes.student import student_bp
    app.register_blueprint(student_bp) 

    # Register scholarship routes
    from routes.scholarship import scholarship_bp
    app.register_blueprint(scholarship_bp) 

    # Register application routes
    from routes.application import application_bp
    app.register_blueprint(application_bp)

    # Register admin routes
    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    # Register chatbot routes
    from routes.chatbot import chatbot_bp
    app.register_blueprint(chatbot_bp)

    # Import all database models
    from models import Student, Scholarship, Application, Admin

    # Homepage
    @app.route("/")
    def home():
        return render_template("index.html")

    # Health check
    @app.route("/health")
    def health():
        return {
            "status": "success",
            "message": "AutoScholar AI is running!"
        }

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
