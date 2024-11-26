# aplicaciones/usuarios/admin.py
from django.contrib import admin
from .models import CustomUser, Rol

admin.site.register(Rol)  # Registrar el modelo Rol
admin.site.register(CustomUser)  # Registrar el modelo CustomUser