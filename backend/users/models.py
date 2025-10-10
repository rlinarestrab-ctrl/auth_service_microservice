import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash seguro
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("rol", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.CharField(
        max_length=20,
        choices=[("admin", "Administrador"), ("estudiante", "Estudiante"), ("orientador", "Orientador")],
        default="estudiante",
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_login = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    # Requeridos por Admin
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # más simple para createsuperuser

    class Meta:
        db_table = "usuarios"

    def __str__(self):
        return f"{self.email} ({self.rol})"


class PerfilEstudiante(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, db_column="usuario_id", related_name="perfil_estudiante"
    )
    intereses = models.TextField(null=True, blank=True)
    habilidades = models.TextField(null=True, blank=True)
    carrera_interes = models.CharField(max_length=100, null=True, blank=True)
    grado_academico = models.CharField(max_length=50, null=True, blank=True)
    institucion_id = models.UUIDField(null=True, blank=True)
    actualmente_estudiando = models.BooleanField(default=False)

    class Meta:
        db_table = "perfiles_estudiantes"
   


class PerfilOrientador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, db_column="usuario_id", related_name="perfil_orientador"
    )
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    experiencia = models.TextField(null=True, blank=True)
    certificaciones = models.TextField(null=True, blank=True)
    institucion_id = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = "perfiles_orientadores"

