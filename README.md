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

| Contraseña | Rol |
|---|---|
| `Admin1234!` | `admin` |

> Los correos son institucionales (@utec.edu.pe).  
> También puedes registrar una cuenta nueva desde `/register`.

---

## 📋 Flujo de Autenticación

```
[0] Registro (opcional)   → /register
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

## 📹 Checklist Video Demostrativo (máx. 5 min)

- [ ] **[0:00]** Mostrar estructura del proyecto en el editor
- [ ] **[0:30]** `docker compose up --build` — esperar arranque
- [ ] **[1:00]** Abrir `http://localhost:5001` → pantalla de login
- [ ] **[1:15]** Mostrar link "¿No tienes cuenta? Regístrate aquí"
- [ ] **[1:30]** Ingresar credenciales admin → ver OTP en logs
- [ ] **[1:50]** Ingresar el código OTP → acceso al panel
- [ ] **[2:10]** Listar usuarios en el dashboard
- [ ] **[2:30]** Crear un nuevo usuario
- [ ] **[3:00]** Editar el usuario creado
- [ ] **[3:20]** Intentar eliminar tu propio admin → bloqueado
- [ ] **[3:35]** Eliminar el usuario creado (modal de confirmación)
- [ ] **[3:55]** Logout → redirección al login

---

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con `scrypt` (Werkzeug)
- ✅ Tokens CSRF en todos los formularios (Flask-WTF)
- ✅ OTP con expiración de 10 minutos en sesión del servidor
- ✅ `@login_required` en todas las rutas del panel
- ✅ Protección contra auto-eliminación del usuario en sesión
- ✅ Registro público con rol `usuario` (no puede auto-asignarse `admin`)
- ✅ Contenedor corriendo como usuario no-root
