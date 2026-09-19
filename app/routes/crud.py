"""CRUD blueprint: user management (list, create, edit, delete)."""
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
)
from flask_login import login_required, current_user
from app import db
from app.models import User
from app.forms import UserCreateForm, UserEditForm

crud_bp = Blueprint("crud", __name__, url_prefix="/users")


@crud_bp.route("/", methods=["GET"])
@login_required
def users_list():
    """Display paginated list of all users."""
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search = request.args.get("q", "").strip()

    query = User.query.order_by(User.created_at.desc())

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            db.or_(User.nombre.ilike(pattern), User.email.ilike(pattern))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items

    return render_template(
        "users/index.html",
        users=users,
        pagination=pagination,
        search=search,
    )


@crud_bp.route("/create", methods=["GET", "POST"])
@login_required
def users_create():
    """Create a new user."""
    form = UserCreateForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()

        # Check for duplicate email
        if User.query.filter_by(email=email).first():
            flash(f"El correo «{email}» ya está registrado.", "danger")
            return render_template("users/create.html", form=form)

        user = User(
            nombre=form.nombre.data.strip(),
            email=email,
            rol=form.rol.data,
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f"Usuario «{user.nombre}» creado exitosamente.", "success")
        return redirect(url_for("crud.users_list"))

    return render_template("users/create.html", form=form)


@crud_bp.route("/<string:user_id>/edit", methods=["GET", "POST"])
@login_required
def users_edit(user_id: str):
    """Edit an existing user."""
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        new_email = form.email.data.strip().lower()

        # Check for duplicate email (exclude current user)
        existing = User.query.filter_by(email=new_email).first()
        if existing and existing.id != user.id:
            flash(f"El correo «{new_email}» ya está en uso por otro usuario.", "danger")
            return render_template("users/edit.html", form=form, user=user)

        user.nombre = form.nombre.data.strip()
        user.email = new_email
        user.rol = form.rol.data

        if form.password.data:
            user.set_password(form.password.data)

        db.session.commit()
        flash(f"Usuario «{user.nombre}» actualizado correctamente.", "success")
        return redirect(url_for("crud.users_list"))

    return render_template("users/edit.html", form=form, user=user)


@crud_bp.route("/<string:user_id>/delete", methods=["POST"])
@login_required
def users_delete(user_id: str):
    """Delete a user. Prevents self-deletion."""
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("No puedes eliminar tu propia cuenta.", "danger")
        return redirect(url_for("crud.users_list"))

    nombre = user.nombre
    db.session.delete(user)
    db.session.commit()

    flash(f"Usuario «{nombre}» eliminado correctamente.", "success")
    return redirect(url_for("crud.users_list"))
