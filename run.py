"""Application entry point.

Runs the database seed on startup to ensure the default admin user exists,
then starts the Flask development server.
For production, the CMD in Dockerfile uses Gunicorn directly.
"""
import subprocess
import sys
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
