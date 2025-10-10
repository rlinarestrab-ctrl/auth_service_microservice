# ===============================
# 🚀 Dockerfile para auth_service
# ===============================
FROM python:3.11-slim

# Evita archivos .pyc y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt gunicorn

# Copiar todo el proyecto
COPY . .

# Exponer puerto (Render asigna dinámico pero declaramos 8000)
ENV PORT=8000
EXPOSE 8000

# Ejecutar migraciones + collectstatic + gunicorn
CMD bash -c "cd backend && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn auth_service.wsgi:application --bind 0.0.0.0:$PORT --timeout 120"





#ANTERIOR DOCKER FILE LOCAL


# FROM python:3.11-slim

# WORKDIR /app

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# RUN chmod +x /app/entrypoint.sh

# EXPOSE 8000
# CMD ["/app/entrypoint.sh"]
