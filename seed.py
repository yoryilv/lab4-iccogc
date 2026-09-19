"""
Seed script: creates the default admin user with a real hashed password.
Run inside the web container or locally:
    docker compose exec web python seed.py
"""
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db
from app.models import User

ADMIN_EMAIL    = "jorge.leandro@utec.edu.pe"
ADMIN_PASSWORD = "Admin1234!"
ADMIN_NAME     = "Administrador"

# ── Extra test users (email, name, role) ──────────────────────────────────────
EXTRA_USERS = [
    ("jfarfan@utec.edu.pe", "J. Farfan", "admin"),
]


def _seed_user(email: str, nombre: str, rol: str, password: str) -> None:
    """Create a user if it doesn't already exist (idempotent)."""
    existing = User.query.filter_by(email=email).first()
    if existing:
        print(f"[seed] '{email}' already exists — skipping.")
        return

    user = User(
        id=str(uuid.uuid4()),
        nombre=nombre,
        email=email,
        rol=rol,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print(f"[seed] ✅ User created: {email} [{rol}]")


def seed():
    app = create_app()
    with app.app_context():
        # Create tables (idempotent)
        db.create_all()

        # Admin user
        existing_admin = User.query.filter_by(email=ADMIN_EMAIL).first()
        if existing_admin:
            print(f"[seed] Admin '{ADMIN_EMAIL}' already exists — skipping.")
            # Fix placeholder hashes if present
            if existing_admin.password_hash.startswith("placeholder") or \
               existing_admin.password_hash.startswith("scrypt:32768:8:1$salt$hash"):
                existing_admin.set_password(ADMIN_PASSWORD)
                db.session.commit()
                print("[seed] Updated admin password hash.")
        else:
            _seed_user(ADMIN_EMAIL, ADMIN_NAME, "admin", ADMIN_PASSWORD)

        # Extra test users (same password for convenience)
        for email, nombre, rol in EXTRA_USERS:
            _seed_user(email, nombre, rol, ADMIN_PASSWORD)


if __name__ == "__main__":
    seed()
