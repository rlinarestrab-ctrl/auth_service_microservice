#!/usr/bin/env bash
set -e

# Esperar a que la DB esté lista
until nc -z ${POSTGRES_HOST:-db} ${POSTGRES_PORT:-5432}; do
  echo "Esperando a la base de datos..."
  sleep 1
done

# No ejecutamos migraciones porque las tablas existen por SQL init (managed=False)
# python manage.py migrate --fake-initial

# Crear super admin/usuario admin si no existe
python manage.py seed_admin

# Ejecutar servidor
python manage.py runserver 0.0.0.0:8000
