"""Utility helpers: OTP generation and email sending."""
import random
import string
import logging
from datetime import datetime, timedelta, timezone
from flask import current_app, session
from flask_mail import Message
from app import mail

logger = logging.getLogger(__name__)


def generate_otp(length: int = 6) -> str:
    """Generate a numeric OTP of the given length."""
    return "".join(random.choices(string.digits, k=length))


def store_otp_in_session(otp: str) -> None:
    """Store the OTP and its expiration timestamp in the server session."""
    expiration_minutes = current_app.config.get("OTP_EXPIRATION_MINUTES", 10)
    session["otp_code"] = otp
    session["otp_expires_at"] = (
        datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    ).isoformat()
    session.modified = True


def verify_otp_from_session(submitted_code: str) -> tuple[bool, str]:
    """
    Validate the submitted OTP against the stored one.

    Returns:
        (is_valid: bool, error_message: str)
    """
    stored_otp = session.get("otp_code")
    expires_at_str = session.get("otp_expires_at")

    if not stored_otp or not expires_at_str:
        return False, "No hay un código OTP activo. Por favor inicia sesión de nuevo."

    expires_at = datetime.fromisoformat(expires_at_str)
    if datetime.now(timezone.utc) > expires_at:
        _clear_otp_from_session()
        return False, "El código OTP ha expirado. Por favor inicia sesión de nuevo."

    if submitted_code.strip() != stored_otp:
        return False, "Código incorrecto. Intenta de nuevo."

    _clear_otp_from_session()
    return True, ""


def _clear_otp_from_session() -> None:
    """Remove OTP data from the session."""
    session.pop("otp_code", None)
    session.pop("otp_expires_at", None)
    session.modified = True


def send_otp_email(recipient_email: str, recipient_name: str, otp: str) -> None:
    """
    Send the OTP to the user's email address.

    In development mode (MAIL_SUPPRESS_SEND=True), the OTP is logged to
    the console so testing works without real SMTP credentials.
    """
    expiration_minutes = current_app.config.get("OTP_EXPIRATION_MINUTES", 10)

    subject = "🔐 Tu código de verificación – Flask Lab"
    body = f"""Hola {recipient_name},

Tu código de verificación de un solo uso es:

    {otp}

Este código es válido por {expiration_minutes} minutos.

Si no solicitaste este código, ignora este correo.

— El equipo de Flask Lab
"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px;">
  <div style="max-width: 480px; margin: 0 auto; background: #1e293b; border-radius: 12px;
              padding: 40px; border: 1px solid #334155;">
    <h2 style="color: #6366f1; margin-bottom: 8px;">🔐 Código de Verificación</h2>
    <p style="color: #94a3b8;">Hola <strong style="color:#e2e8f0">{recipient_name}</strong>,</p>
    <p style="color: #94a3b8;">Tu código de verificación de un solo uso es:</p>
    <div style="background: #0f172a; border: 2px solid #6366f1; border-radius: 8px;
                padding: 20px; text-align: center; margin: 24px 0;">
      <span style="font-size: 48px; font-weight: bold; color: #6366f1;
                   letter-spacing: 12px;">{otp}</span>
    </div>
    <p style="color: #94a3b8; font-size: 14px;">
      ⏱ Este código expira en <strong style="color:#e2e8f0">{expiration_minutes} minutos</strong>.
    </p>
    <p style="color: #64748b; font-size: 12px; margin-top: 32px;">
      Si no solicitaste este código, ignora este correo de forma segura.
    </p>
  </div>
</body>
</html>
"""

    suppress = current_app.config.get("MAIL_SUPPRESS_SEND", True)

    # Always log the OTP for development convenience
    logger.warning(
        "\n" + "=" * 60 +
        f"\n  OTP para {recipient_email}: {otp}" +
        f"\n  Expira en: {expiration_minutes} minutos" +
        "\n" + "=" * 60
    )

    if suppress:
        print(
            f"\n{'='*60}\n"
            f"  [DEV MODE] OTP para {recipient_email}\n"
            f"  Código: {otp}\n"
            f"  Expira en: {expiration_minutes} min\n"
            f"{'='*60}\n"
        )
        return

    msg = Message(
        subject=subject,
        recipients=[recipient_email],
        body=body,
        html=html_body,
    )
    try:
        mail.send(msg)
        logger.info(f"OTP email sent to {recipient_email}")
    except Exception as exc:
        logger.error(f"Failed to send OTP email to {recipient_email}: {exc}")
        raise
