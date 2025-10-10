# Auth Service (Django + DRF + JWT) + React (Login & CRUD)

Microservicio de autenticación/usuarios para tu proyecto de orientación vocacional.

## Requisitos
- Docker y Docker Compose

## Cómo ejecutar
```bash
docker compose up --build
```
- Backend Django disponible en: http://localhost:8000
- Frontend React (Vite) en: http://localhost:5173

> El servicio de base de datos se inicializa con el script SQL provisto y crea las tablas con `uuid-ossp`.
> El backend usa modelos `managed=False` para mapearse a las tablas existentes y **no** ejecuta migraciones.

## Credenciales de prueba
Se crea (si no existe) un usuario admin mediante variables de entorno:
- Email: `admin@example.com`
- Password: `admin123`

Puedes cambiarlas en `docker-compose.yml`.

## Endpoints principales
- `POST /api/auth/register` – registro de usuario
- `POST /api/auth/login` – login con JWT
- `POST /api/auth/refresh` – refrescar token
- `GET /api/users` – listar usuarios (admin)
- `POST /api/users` – crear usuario (admin)
- `GET /api/users/{id}` – obtener detalle (admin o el propio usuario)
- `PUT/PATCH /api/users/{id}` – actualizar (admin o el propio usuario)
- `DELETE /api/users/{id}` – eliminar (admin)

## Frontend
Incluye:
- Pantalla de Login
- Listado de usuarios (con paginación simple)
- Crear/editar/eliminar usuarios (solo si rol=admin)

## Notas
- Las contraseñas se guardan como `password_hash` usando `PBKDF2` de Django.
- El modelo de base de datos respeta tu ERD (tablas `usuarios`, `perfiles_estudiantes`, `perfiles_orientadores`).
- CORS configurado para `http://localhost:5173` por defecto.
