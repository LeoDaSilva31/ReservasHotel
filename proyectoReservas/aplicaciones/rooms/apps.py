# aplicaciones/rooms/apps.py
from django.apps import AppConfig

class RoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplicaciones.rooms' 
    verbose_name = 'Habitaciones'