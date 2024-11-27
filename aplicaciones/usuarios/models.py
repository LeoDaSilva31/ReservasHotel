# aplicaciones/usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models

class Rol(models.Model):
    # Modelo para los roles de usuario (Gerente, Propietario, Recepcionista)
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    # Modelo personalizado de usuario que extiende el usuario base de Django
    
    # Campos personalizados adicionales
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    # Relación con el modelo Rol (puede ser nulo si se elimina el rol)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Sobreescribimos el método save para asegurar que las contraseñas se hasheen
        # Verifica si la contraseña no está hasheada (no comienza con los prefijos de hash conocidos)
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        # Representación en string del usuario
        return f"{self.nombre} {self.apellido} ({self.username})"