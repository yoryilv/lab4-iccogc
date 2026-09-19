# 🔐 Flask Lab – Autenticación 2FA + CRUD de Usuarios

> **Laboratorio 4 – Desarrollo de Aplicación Flask**  
> Autenticación de dos factores (OTP por correo), registro de usuarios, panel de administración y CRUD completo, contenerizado con Docker + PostgreSQL.

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
> También puedes registrar una cuenta nueva desde `/register`.

---

## 📋 Flujo de Autenticación

```
[0] Registro (opcional)    → /register
[1] Login email + password → /login
[2] Código OTP enviado al correo (ver logs si MAIL_SUPPRESS_SEND=True)
[3] Verificación OTP       → /verify-otp
[4] Acceso al panel        → /users
```

**Ver OTP en logs (modo desarrollo):**
```bash
docker compose logs -f web
```

---

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con `scrypt` (Werkzeug)
- ✅ Tokens CSRF en todos los formularios (Flask-WTF)
- ✅ OTP con expiración de 10 minutos en sesión del servidor
- ✅ `@login_required` en todas las rutas del panel
- ✅ Protección contra auto-eliminación del usuario en sesión
- ✅ Registro público con rol `usuario` (no puede auto-asignarse `admin`)
- ✅ Contenedor corriendo como usuario no-root

---

## 🐛 Solución de Problemas

**Docker no arranca:**
```bash
open -a Docker   # Abrir Docker Desktop en macOS
```

**La app no conecta a la BD:**
```bash
docker compose ps          # Verificar estado de contenedores
docker compose restart web # Reiniciar solo el web
```

**No aparece el OTP en logs:**
```bash
# Verificar que MAIL_SUPPRESS_SEND=True en .env
docker compose logs web | grep -A3 "======"
```

**No puedo cerrar sesión:**
```bash
docker compose exec web sh -c "rm -rf /tmp/flask_session/*"
docker compose restart web
```
