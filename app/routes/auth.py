"""Authentication blueprint: login, OTP verification, logout."""
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request,
    current_app,
)
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import LoginForm, OTPForm, RegisterForm
from app.utils import generate_otp, store_otp_in_session, verify_otp_from_session, send_otp_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET"])
def index():
    """Root redirect: send authenticated users to dashboard, others to login."""
    if current_user.is_authenticated:
        return redirect(url_for("crud.users_list"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Public user registration.
    Validates required fields, verifies email uniqueness, hashes password,
    and redirects to login upon success.
    """
    if current_user.is_authenticated:
        return redirect(url_for("crud.users_list"))

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()

        # Check for duplicate email
        if User.query.filter_by(email=email).first():
            flash(
                f"El correo «{email}» ya se encuentra registrado. Por favor inicia sesión o usa otro correo.",
                "danger",
            )
            return render_template("register.html", form=form)

        user = User(
            nombre=form.nombre.data.strip(),
            email=email,
            rol=form.rol.data,
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(
            f"¡Cuenta creada con éxito para {user.nombre}! Por favor inicia sesión.",
            "success",
        )
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Step 1 of authentication: validate credentials.
    On success, generate OTP, send email and redirect to verify step.
    """
    if current_user.is_authenticated:
        return redirect(url_for("crud.users_list"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("Credenciales incorrectas. Verifica tu correo y contraseña.", "danger")
            return render_template("login.html", form=form)

        # Credentials valid → generate and store OTP
        otp = generate_otp()
        store_otp_in_session(otp)

        # Store the pending user id (not authenticated yet)
        session["pending_user_id"] = user.id
        session.modified = True

        # Send OTP by email (printed to console in dev mode)
        try:
            send_otp_email(user.email, user.nombre, otp)
        except Exception as exc:
            current_app.logger.error(f"Error sending OTP: {exc}")
            flash(
                "No se pudo enviar el código de verificación. Intenta de nuevo.",
                "danger",
            )
            return render_template("login.html", form=form)

        flash(
            f"Código de verificación enviado a {user.email}. "
            "Revisa también la consola del servidor en modo desarrollo.",
            "info",
        )
        return redirect(url_for("auth.verify_otp"))

    return render_template("login.html", form=form)


@auth_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    """
    Step 2 of authentication: validate the OTP code.
    On success, creates the authenticated session.
    """
    # If already authenticated, go to dashboard
    if current_user.is_authenticated:
        return redirect(url_for("crud.users_list"))

    # Ensure step 1 was completed
    pending_user_id = session.get("pending_user_id")
    if not pending_user_id:
        flash("Por favor inicia sesión primero.", "warning")
        return redirect(url_for("auth.login"))

    form = OTPForm()

    if form.validate_on_submit():
        submitted_code = form.otp_code.data.strip()
        is_valid, error_msg = verify_otp_from_session(submitted_code)

        if not is_valid:
            flash(error_msg, "danger")
            # If OTP expired, clear session and force re-login
            if "expirado" in error_msg or "No hay" in error_msg:
                session.pop("pending_user_id", None)
                return redirect(url_for("auth.login"))
            return render_template("verify_otp.html", form=form)

        # OTP valid → complete login
        user = User.query.get(pending_user_id)
        if user is None:
            flash("Usuario no encontrado. Por favor inicia sesión de nuevo.", "danger")
            session.pop("pending_user_id", None)
            return redirect(url_for("auth.login"))

        session.pop("pending_user_id", None)
        login_user(user, remember=False)
        flash(f"¡Bienvenido, {user.nombre}!", "success")

        next_page = request.args.get("next")
        return redirect(next_page or url_for("crud.users_list"))

    # Calculate remaining OTP time for the countdown display
    otp_expiration_minutes = current_app.config.get("OTP_EXPIRATION_MINUTES", 10)

    return render_template(
        "verify_otp.html",
        form=form,
        otp_expiration_minutes=otp_expiration_minutes,
    )


@auth_bp.route("/logout")
@login_required
def logout():
    """Invalidate session and redirect to login."""
    nombre = current_user.nombre
    logout_user()
    # Explicitly remove all session data (needed for Flask-Session filesystem backend)
    session.clear()
    for key in list(session.keys()):
        session.pop(key, None)
    flash(f"Hasta luego, {nombre}. Tu sesión ha sido cerrada.", "info")
    return redirect(url_for("auth.login"))
