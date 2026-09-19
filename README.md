# 🔐 Flask Lab – Autenticación 2FA + CRUD de Usuarios

> **Laboratorio 4 – Desarrollo de Aplicación Flask**  
> Aplicación web con autenticación de dos factores (OTP por correo), registro público de usuarios, panel de administración y CRUD completo, contenerizado con Docker + PostgreSQL.

---

## 🚀 Levantar el proyecto

```bash
docker compose up --build
```

Acceder en: **http://localhost:5001**

---

## 🔑 Credenciales

Contraseña general: **`Admin1234!`**

> Los correos son institucionales (@utec.edu.pe).  
> Puedes registrar un nuevo usuario desde la pestaña **"Crear Cuenta"** en la pantalla de inicio (`/register`).

---

## 📋 Flujo de Autenticación

```
[0] Registro de usuario    → /register (o pestaña "Crear Cuenta" en el login)
[1] Login email + password → /login
[2] Código OTP enviado al correo (ver logs en modo desarrollo)
[3] Verificación OTP       → /verify-otp
[4] Acceso al panel CRUD   → /users
```

**Ver OTP en logs (modo desarrollo):**
```bash
docker compose logs -f web
```

---

## 👥 Funcionalidades CRUD (Rúbrica)

- **Crear (2 pts):** Formulario para registrar un nuevo usuario desde `/register` (pantalla de inicio) o `/users/create`, con validación estricta de campos obligatorios, formato de correo y confirmación de contraseña.
- **Leer (2 pts):** Listado paginado de todos los usuarios en una tabla con buscador por nombre y correo (`/users/`).
- **Actualizar (3 pts):** Posibilidad de editar los datos de un usuario (nombre, correo, rol y actualización opcional de contraseña) (`/users/<id>/edit`).
- **Eliminar (3 pts):** Botón para eliminar un usuario con modal interactivo de confirmación y protección que impide la auto-eliminación de la cuenta en sesión.

---

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con algoritmo seguro `scrypt` (Werkzeug)
- ✅ Tokens CSRF en todos los formularios (Flask-WTF)
- ✅ OTP de 6 dígitos con expiración de 10 minutos
- ✅ `@login_required` en todas las rutas protegidas del panel
- ✅ Protección contra auto-eliminación del usuario activo
- ✅ Validación y sanitización de entradas tanto en cliente como en servidor
- ✅ Contenedor Docker ejecutándose con usuario no-root

---

## 🐛 Solución de Problemas

**Docker no arranca:**
```bash
open -a Docker   # Abrir Docker Desktop en macOS
```

**La app no conecta a la BD:**
```bash
docker compose ps          # Verificar estado de contenedores
docker compose restart web # Reiniciar solo el contenedor web
```

**No aparece el OTP en logs:**
```bash
# Verificar logs de envío/generación de OTP
docker compose logs web | grep -A3 "======"
```

**No puedo cerrar sesión / Limpiar sesiones:**
```bash
docker compose exec web sh -c "rm -rf /tmp/flask_session/*"
docker compose restart web
```
