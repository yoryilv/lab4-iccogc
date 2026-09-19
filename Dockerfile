# ════════════════════════════════════════════
#  Flask Lab – Dockerfile
#  Python 3.11 slim + Gunicorn
# ════════════════════════════════════════════

# Pin to Bookworm (Debian stable) — avoids broken Trixie apt repos
FROM python:3.11-slim-bookworm

# Metadata
LABEL maintainer="Flask Lab" \
      version="1.0" \
      description="Flask Lab – Autenticación 2FA + CRUD de Usuarios"

# ── No system dependencies needed ────────────────────────────────────
# psycopg2-binary ships pre-compiled binaries (no gcc / libpq-dev needed)

# ── Working directory ─────────────────────────────────────────────────
WORKDIR /app

# ── Python dependencies ───────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Application code ──────────────────────────────────────────────────
COPY . .

# ── Flask session directory ───────────────────────────────────────────
RUN mkdir -p /tmp/flask_session

# ── Make entrypoint executable ────────────────────────────────────────
RUN chmod +x entrypoint.sh

# ── Non-root user for security ────────────────────────────────────────
RUN addgroup --system flaskgroup && adduser --system --ingroup flaskgroup flaskuser
RUN chown -R flaskuser:flaskgroup /app /tmp/flask_session
USER flaskuser

# ── Expose port ───────────────────────────────────────────────────────
EXPOSE 5000

# ── Health check (pure Python — no curl needed) ──────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request, sys; urllib.request.urlopen('http://localhost:5000/') or sys.exit(1)" || exit 1

# ── Start command ─────────────────────────────────────────────────────
CMD ["./entrypoint.sh"]
