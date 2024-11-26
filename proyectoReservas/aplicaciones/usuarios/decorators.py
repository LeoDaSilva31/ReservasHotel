# aplicaciones/usuarios/decorators.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib import messages

def login_not_required(view_func):
    """
    Decorador para redirigir usuarios ya autenticados.
    Útil para páginas como login donde usuarios autenticados no deberían acceder.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('reservations')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def superuser_required(view_func):
    """Decorador para vistas que solo el superusuario puede acceder"""
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Acceso denegado. Se requieren permisos de administrador.')
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return _wrapped_view

def gerente_required(view_func):
    """Decorador para vistas que requieren rol de gerente"""
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or (request.user.rol and request.user.rol.nombre == 'Gerente'):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Acceso denegado. Se requiere rol de Gerente.')
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return _wrapped_view

def propietario_required(view_func):
    """Decorador para vistas que requieren rol de propietario"""
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or (request.user.rol and request.user.rol.nombre == 'Propietario'):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Acceso denegado. Se requiere rol de Propietario.')
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return _wrapped_view

def recepcionista_required(view_func):
    """Decorador para vistas que requieren rol de recepcionista"""
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or (request.user.rol and request.user.rol.nombre == 'Recepcionista'):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Acceso denegado. Se requiere rol de Recepcionista.')
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return _wrapped_view

def user_is_active_required(view_func):
    """Decorador para asegurar que el usuario esté activo"""
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_active:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Tu cuenta está desactivada.')
        return HttpResponseForbidden("Tu cuenta está desactivada.")
    return _wrapped_view