"""WTForms form definitions."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, HiddenField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    ValidationError,
)


class LoginForm(FlaskForm):
    """User login form."""

    email = StringField(
        "Correo Electrónico",
        validators=[DataRequired(message="El correo es obligatorio."), Email()],
        render_kw={"placeholder": "tu@correo.com", "autocomplete": "email"},
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=6, message="Mínimo 6 caracteres."),
        ],
        render_kw={"placeholder": "••••••••"},
    )
    submit = SubmitField("Iniciar Sesión")


class OTPForm(FlaskForm):
    """One-time password verification form."""

    otp_code = StringField(
        "Código de Verificación",
        validators=[
            DataRequired(message="Ingresa el código OTP."),
            Length(min=6, max=6, message="El código debe tener exactamente 6 dígitos."),
        ],
        render_kw={"placeholder": "000000", "maxlength": "6", "inputmode": "numeric"},
    )
    submit = SubmitField("Verificar Código")


class UserCreateForm(FlaskForm):
    """Form for creating a new user."""

    nombre = StringField(
        "Nombre Completo",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=120),
        ],
        render_kw={"placeholder": "Juan Pérez"},
    )
    email = StringField(
        "Correo Electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingresa un correo válido."),
            Length(max=255),
        ],
        render_kw={"placeholder": "juan@ejemplo.com"},
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=8, message="Mínimo 8 caracteres."),
        ],
        render_kw={"placeholder": "Mínimo 8 caracteres"},
    )
    confirm_password = PasswordField(
        "Confirmar Contraseña",
        validators=[
            DataRequired(message="Confirma la contraseña."),
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
        render_kw={"placeholder": "Repite la contraseña"},
    )
    rol = SelectField(
        "Rol",
        choices=[("usuario", "Usuario"), ("admin", "Administrador")],
        default="usuario",
    )
    submit = SubmitField("Crear Usuario")


class UserEditForm(FlaskForm):
    """Form for editing an existing user."""

    nombre = StringField(
        "Nombre Completo",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=120),
        ],
    )
    email = StringField(
        "Correo Electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingresa un correo válido."),
            Length(max=255),
        ],
    )
    password = PasswordField(
        "Nueva Contraseña (dejar en blanco para no cambiar)",
        validators=[
            Optional(),
            Length(min=8, message="Mínimo 8 caracteres."),
        ],
        render_kw={"placeholder": "Dejar en blanco para no cambiar"},
    )
    confirm_password = PasswordField(
        "Confirmar Nueva Contraseña",
        validators=[
            Optional(),
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
    )
    rol = SelectField(
        "Rol",
        choices=[("usuario", "Usuario"), ("admin", "Administrador")],
    )
    submit = SubmitField("Guardar Cambios")
