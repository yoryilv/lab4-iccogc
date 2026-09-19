-- ════════════════════════════════════════════════════
--  Flask Lab – Database Seed Script
--  Ejecutado automáticamente por PostgreSQL al crear
--  la base de datos por primera vez en Docker.
-- ════════════════════════════════════════════════════

-- Create ENUM type for roles (SQLAlchemy also creates it, but this ensures
-- it exists before the app runs in case of timing issues)
DO $$ BEGIN
    CREATE TYPE user_roles AS ENUM ('admin', 'usuario');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- Create users table (mirrors the SQLAlchemy model)
CREATE TABLE IF NOT EXISTS users (
    id          VARCHAR(36)  PRIMARY KEY,
    nombre      VARCHAR(120) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    rol         user_roles   NOT NULL DEFAULT 'usuario',
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);

-- ── Trigger: auto-update updated_at ──────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON users;
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ── Seed: default admin user ──────────────────────────────────────────
-- Email   : admin@lab.com
-- Password: Admin1234!
-- Hash    : werkzeug pbkdf2:sha256 (generated with generate_password_hash)
INSERT INTO users (id, nombre, email, password_hash, rol, created_at, updated_at)
VALUES (
    gen_random_uuid()::text,
    'Administrador',
    'admin@lab.com',
    'scrypt:32768:8:1$salt$hash_placeholder',
    'admin',
    NOW(),
    NOW()
)
ON CONFLICT (email) DO NOTHING;

-- NOTE: The password hash above is a placeholder.
-- The actual hashed password is inserted by the Flask app on startup.
-- See the note in README.md for the correct seeding approach.

-- ── Additional demo users ─────────────────────────────────────────────
INSERT INTO users (id, nombre, email, password_hash, rol, created_at, updated_at)
VALUES
(
    gen_random_uuid()::text,
    'María García',
    'maria@lab.com',
    'placeholder_hash',
    'usuario',
    NOW() - INTERVAL '5 days',
    NOW() - INTERVAL '5 days'
),
(
    gen_random_uuid()::text,
    'Carlos López',
    'carlos@lab.com',
    'placeholder_hash',
    'usuario',
    NOW() - INTERVAL '3 days',
    NOW() - INTERVAL '3 days'
)
ON CONFLICT (email) DO NOTHING;
