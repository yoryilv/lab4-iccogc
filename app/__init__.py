"""Flask Application Factory."""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_session import Session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─── Extension Instances ──────────────────────────────────────────────────────
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
sess = Session()


def create_app() -> Flask:
    """Application factory pattern."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ── Configuration ──────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "postgresql://flaskuser:flaskpassword@db:5432/flasklab"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Session configuration
    app.config["SESSION_TYPE"] = os.environ.get("SESSION_TYPE", "filesystem")
    app.config["SESSION_FILE_DIR"] = os.environ.get(
        "SESSION_FILE_DIR", "/tmp/flask_session"
    )
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True

    # Flask-Mail configuration
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "True") == "True"
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get(
        "MAIL_DEFAULT_SENDER", "noreply@flasklab.com"
    )
    app.config["MAIL_SUPPRESS_SEND"] = (
        os.environ.get("MAIL_SUPPRESS_SEND", "True") == "True"
    )

    # OTP configuration
    app.config["OTP_EXPIRATION_MINUTES"] = int(
        os.environ.get("OTP_EXPIRATION_MINUTES", 10)
    )

    # ── Initialize Extensions ──────────────────────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    sess.init_app(app)

    # ── Login Manager ──────────────────────────────────────────────────────────
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor inicia sesión para acceder a esta página."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id: str):
        from app.models import User
        return User.query.get(user_id)

    # ── Register Blueprints ────────────────────────────────────────────────────
    from app.routes.auth import auth_bp
    from app.routes.crud import crud_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(crud_bp)

    # ── Create tables if not exist (fallback) ─────────────────────────────────
    with app.app_context():
        db.create_all()

    return app
