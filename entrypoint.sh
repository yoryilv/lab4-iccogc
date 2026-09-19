#!/bin/sh
# ════════════════════════════════════════════
#  Docker entrypoint script
#  1. Run database seed (creates admin user)
#  2. Start Gunicorn
# ════════════════════════════════════════════

set -e

echo "⏳ Running database seed..."
python seed.py

echo "🚀 Starting Gunicorn..."
exec gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  run:app
