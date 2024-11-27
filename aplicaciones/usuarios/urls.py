# aplicaciones/usuarios/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'usuarios'  # Esto hace que necesitemos usar usuarios:nombre_url en los templates

urlpatterns = [
    # Rutas de autenticación
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', LogoutView.as_view(next_page='usuarios:iniciar_sesion'), name='logout'),
    
    # Gestión de usuarios
    path('gestionar-usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('editar-usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    
    # Perfil de usuario
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # Rutas adicionales
    path('usuarios/buscar/', views.gestionar_usuarios, name='buscar_usuarios'),
]