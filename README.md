# 🔐 Flask Lab – Autenticación 2FA + CRUD de Usuarios

> **Laboratorio 4 – Desarrollo de Aplicación Flask**  
> Aplicación web con autenticación de dos factores (OTP por correo), registro de usuarios, panel de administración y CRUD completo, todo contenerizado con Docker + PostgreSQL.

---

## 🏗️ Arquitectura del Proyecto

```
flask-lab/
├── app/
│   ├── __init__.py          # App factory (Flask + extensiones)
│   ├── models.py            # Modelo User (SQLAlchemy)
│   ├── forms.py             # WTForms (Login, OTP, Register, CRUD)
│   ├── utils.py             # Helpers OTP (generar, validar, enviar)
│   ├── routes/
│   │   ├── auth.py          # Blueprint: /login, /register, /verify-otp, /logout
│   │   └── crud.py          # Blueprint: /users (CRUD completo)
│   ├── templates/
│   │   ├── base.html        # Layout principal (sidebar + topbar)
│   │   ├── login.html       # Pantalla de login
│   │   ├── register.html    # Registro de nueva cuenta
│   │   ├── verify_otp.html  # Verificación OTP con countdown
│   │   └── users/
│   │       ├── index.html   # Tabla de usuarios + paginación
│   │       ├── create.html  # Formulario de creación
│   │       └── edit.html    # Formulario de edición
│   └── static/css/
│       └── custom.css       # Tema oscuro premium
├── seed.py                  # Script de semilla (admin + usuarios de prueba)
├── entrypoint.sh            # Docker entrypoint (seed + gunicorn)
├── init.sql                 # Inicialización SQL de PostgreSQL
├── run.py                   # Servidor de desarrollo
├── .env                     # Variables de entorno (NO commitear)
├── .env.example             # Plantilla de variables de entorno
├── requirements.txt         # Dependencias Python
├── Dockerfile               # Imagen del contenedor Flask (python:3.11-slim-bookworm)
└── docker-compose.yml       # Orquestación: db + web (puerto 5001)
```

---

## 🚀 Inicio Rápido con Docker

### Prerrequisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y **en ejecución**
- [Docker Compose](https://docs.docker.com/compose/) v2+

### 1. Clonar / descargar el proyecto

```bash
cd /ruta/a/tu/proyecto/lab4
```

### 2. Configurar variables de entorno

El archivo `.env` ya viene configurado con valores por defecto para desarrollo. Para usar SMTP real:

```bash
# Editar el .env y configurar credenciales de correo
MAIL_SUPPRESS_SEND=False          # Activar envío real de correos
MAIL_USERNAME=tu@gmail.com        # Tu correo Gmail
MAIL_PASSWORD=tu_app_password     # App Password de Google
```

> **💡 En modo desarrollo** (`MAIL_SUPPRESS_SEND=True`): el código OTP se imprime directamente en la consola/logs del contenedor `web`. No necesitas configurar SMTP.

### 3. Levantar el proyecto

```bash
docker compose up --build
```

La primera vez tomará ~1-2 minutos para:
1. Descargar imágenes de Docker
2. Instalar dependencias Python (sin apt-get — `psycopg2-binary` no necesita compilación)
3. Inicializar PostgreSQL con el script SQL
4. Ejecutar el seed de usuarios
5. Iniciar Gunicorn

### 4. Acceder a la aplicación

Abre tu navegador en: **http://localhost:5001**

---

## 🔑 Credenciales por Defecto

| Email | Contraseña | Rol |
|---|---|---|
| `jorge.leandro@utec.edu.pe` | `Admin1234!` | `admin` |
| `jfarfan@utec.edu.pe` | `Admin1234!` | `admin` |

> Puedes crear más cuentas desde la pantalla de **Registro** (`/register`) sin necesidad de acceso previo.

---

## 📋 Flujo de Autenticación

```
[0] Registro (opcional) → /register
         ↓ Cuenta creada con rol "usuario"
[1] Login (email + password) → /login
         ↓ Credenciales válidas
[2] Generación OTP (6 dígitos, 10 min de validez)
         ↓ Código enviado por email / impreso en consola
[3] Verificación OTP → /verify-otp (countdown visible)
         ↓ Código correcto
[4] Sesión iniciada → Dashboard /users
```

### Ver el código OTP en Docker

```bash
# Ver logs del contenedor web (el OTP aparece ahí)
docker compose logs -f web

# Buscar específicamente el OTP
docker compose logs web | grep "OTP para"
```

---

## 🗂️ CRUD de Usuarios

| Operación | Ruta | Descripción |
|---|---|---|
| Listar | `GET /users/` | Tabla paginada con búsqueda |
| Crear | `GET/POST /users/create` | Formulario con validación completa |
| Editar | `GET/POST /users/<id>/edit` | Formulario precargado |
| Eliminar | `POST /users/<id>/delete` | Con confirmación modal; protege auto-eliminación |

> Todas las rutas `/users/*` requieren `@login_required`.

---

## ⚙️ Variables de Entorno

| Variable | Default | Descripción |
|---|---|---|
| `SECRET_KEY` | *(valor de ejemplo)* | Clave secreta de Flask |
| `DATABASE_URL` | `postgresql://flaskuser:...@db/...` | URL de conexión a PostgreSQL |
| `POSTGRES_USER` | `flaskuser` | Usuario de la BD |
| `POSTGRES_PASSWORD` | `flaskpassword` | Contraseña de la BD |
| `POSTGRES_DB` | `flasklab` | Nombre de la BD |
| `MAIL_SERVER` | `smtp.gmail.com` | Servidor SMTP |
| `MAIL_PORT` | `587` | Puerto SMTP |
| `MAIL_USERNAME` | *(vacío)* | Usuario SMTP |
| `MAIL_PASSWORD` | *(vacío)* | Contraseña SMTP |
| `MAIL_SUPPRESS_SEND` | `True` | `True` = solo consola; `False` = envío real |
| `OTP_EXPIRATION_MINUTES` | `10` | Tiempo de validez del OTP |

---

## 🛠️ Comandos Útiles

```bash
# Levantar en background
docker compose up -d --build

# Ver logs en tiempo real
docker compose logs -f

# Ver solo logs del web (con OTP)
docker compose logs -f web

# Ejecutar seed manualmente (añade admin + usuarios de prueba)
docker compose exec web python seed.py

# Acceder a la BD
docker compose exec db psql -U flaskuser -d flasklab

# Listar usuarios en la BD
docker compose exec db psql -U flaskuser -d flasklab -c "SELECT nombre, email, rol FROM users;"

# Detener todo
docker compose down

# Detener y eliminar volúmenes (reset completo de la BD)
docker compose down -v
```

---

## 📹 Checklist para Video Demostrativo (máx. 5 min)

- [ ] **[0:00]** Mostrar estructura del proyecto en el editor
- [ ] **[0:30]** Ejecutar `docker compose up --build` y esperar el arranque
- [ ] **[1:00]** Acceder a `http://localhost:5001` → pantalla de login
- [ ] **[1:10]** Mostrar el link "¿No tienes cuenta? Regístrate aquí"
- [ ] **[1:20]** Ingresar credenciales admin → ingresar el OTP
- [ ] **[1:30]** Mostrar logs con el código OTP (`docker compose logs -f web`)
- [ ] **[1:45]** Ingresar el código OTP → acceso al panel
- [ ] **[2:00]** Listar usuarios en la tabla del dashboard
- [ ] **[2:20]** Crear un nuevo usuario con el formulario
- [ ] **[2:50]** Editar el usuario recién creado
- [ ] **[3:10]** Intentar eliminar al admin propio → mostrar que está bloqueado
- [ ] **[3:25]** Eliminar el usuario creado con modal de confirmación
- [ ] **[3:45]** Logout → redirección a login
- [ ] **[4:00]** Mostrar docker-compose.yml y Dockerfile brevemente
- [ ] **[4:30]** Mostrar el .env.example con variables de configuración

---

## 🔒 Seguridad Implementada

- ✅ Contraseñas hasheadas con `scrypt` (Werkzeug)
- ✅ Tokens CSRF en todos los formularios (Flask-WTF)
- ✅ OTP con expiración de 10 minutos almacenado en sesión del servidor
- ✅ `@login_required` en todas las rutas del panel
- ✅ Protección contra auto-eliminación del usuario en sesión
- ✅ Validación de email único en base de datos
- ✅ Registro público con rol `usuario` (sin poder auto-asignarse `admin`)
- ✅ Contenedor corriendo como usuario no-root
- ✅ Variables sensibles en `.env` (no commiteado)

---

## 🐛 Solución de Problemas

**Docker no arranca (`docker.sock` no encontrado):**
```bash
# Asegúrate de que Docker Desktop esté abierto
open -a Docker
```

**La app no conecta a la BD:**
```bash
# Verificar que la BD esté healthy
docker compose ps
# Reiniciar el servicio web
docker compose restart web
```

**Error \"relation users does not exist\":**
```bash
# Ejecutar seed manualmente
docker compose exec web python seed.py
```

**No aparece el OTP en logs:**
```bash
# Asegúrate que MAIL_SUPPRESS_SEND=True en .env
docker compose logs web | grep -A3 "======"
```

**No puedo cerrar sesión:**
```bash
# Limpiar sesiones del servidor manualmente si persiste
docker compose exec web rm -rf /tmp/flask_session/*
docker compose restart web
```
