"""Database models for the Flask application."""
import uuid
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


def _utcnow() -> datetime:
    """Return current UTC datetime (timezone-aware)."""
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    """User model for authentication and CRUD management."""

    __tablename__ = "users"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(
        db.Enum("admin", "usuario", name="user_roles"),
        nullable=False,
        default="usuario",
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
        onupdate=_utcnow,
    )

    # ── Constructor ────────────────────────────────────────────────────────────

    def __init__(self, **kwargs) -> None:
        """Accept column names as keyword arguments (SQLAlchemy convention)."""
        super().__init__(**kwargs)

    # ── Password helpers ───────────────────────────────────────────────────────

    def set_password(self, password: str) -> None:
        """Hash and store the user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    # ── Role helpers ───────────────────────────────────────────────────────────

    @property
    def is_admin(self) -> bool:
        """Return True if the user has admin role."""
        return self.rol == "admin"

    # ── Flask-Login compatibility ──────────────────────────────────────────────

    def get_id(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return f"<User {self.email} [{self.rol}]>"
