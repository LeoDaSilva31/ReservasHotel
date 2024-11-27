   # mi_proyecto/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('aplicaciones.home.urls')),  # Incluir URLs de home
       path('usuarios/', include('aplicaciones.usuarios.urls')),  # Incluir URLs de usuarios
       path('reservations/', include('aplicaciones.reservations.urls', namespace='reservations')),
   ]