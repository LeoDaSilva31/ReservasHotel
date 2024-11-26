# aplicaciones/usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import CustomUser, Rol
from .forms import CustomUserCreationForm, CustomUserChangeForm
import logging

logger = logging.getLogger(__name__)

def iniciar_sesion(request):
    """Vista para el inicio de sesión de usuarios"""
    # Redirigir si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('reservations')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        logger.debug(f"Intento de login para usuario: {username}")
        
        # Intenta autenticar al usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            logger.debug(f"Usuario autenticado: {user.username}, is_active: {user.is_active}")
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', '/reservations/')
                return redirect(next_url)
            else:
                logger.warning(f"Intento de login con cuenta desactivada: {username}")
                messages.error(request, 'Su cuenta está desactivada.')
        else:
            logger.warning(f"Fallo de autenticación para usuario: {username}")
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    
    return render(request, 'usuarios/iniciar_sesion.html')

@login_required
@login_required
def gestionar_usuarios(request):
    # Manejo del buscador
    query = request.GET.get('q', '')
    if query:
        usuarios = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query)
        ).order_by('username')
    else:
        usuarios = CustomUser.objects.all().order_by('username')

    if request.method == 'POST':
        if 'delete' in request.POST:
            user_id = request.POST.get('user_id')
            try:
                user = CustomUser.objects.get(id=user_id)
                if user == request.user:
                    messages.error(request, 'No puedes eliminar tu propia cuenta.')
                else:
                    user.delete()
                    messages.success(request, 'Usuario eliminado con éxito.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')
            return redirect('usuarios:gestionar_usuarios')
            
        elif 'create' in request.POST:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuario creado con éxito.')
                return redirect('usuarios:gestionar_usuarios')
    else:
        form = CustomUserCreationForm()

    context = {
        'usuarios': usuarios,
        'query': query,
        'form': form,
        'show_modal': request.method == 'POST' and 'create' in request.POST and not form.is_valid(),  # Nueva variable
        'total_usuarios': usuarios.count()
    }
    return render(request, 'usuarios/gestionar_usuarios.html', context)

@login_required
def editar_usuario(request, id):
    """Vista para editar un usuario existente"""
    usuario = get_object_or_404(CustomUser, id=id)
    
    # Verificar si el usuario actual tiene permiso para editar
    if not request.user.is_superuser and request.user != usuario:
        messages.error(request, 'No tienes permiso para editar este usuario.')
        return redirect('gestionar_usuarios')

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            # Si se está editando el usuario actual, asegurarse de que no se desactive
            if usuario == request.user and not form.cleaned_data.get('is_active'):
                form.cleaned_data['is_active'] = True
                messages.warning(request, 'No puedes desactivar tu propia cuenta.')
            
            form.save()
            messages.success(request, 'Usuario actualizado con éxito.')
            return redirect('gestionar_usuarios')
        else:
            # Mostrar errores de validación
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserChangeForm(instance=usuario)
    
    return render(request, 'usuarios/editar_usuario.html', {
        'form': form,
        'usuario': usuario,
        'es_usuario_actual': usuario == request.user
    })

@login_required
def perfil_usuario(request):
    """Vista para que un usuario vea y edite su propio perfil"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            # Asegurarse de que el usuario no pueda desactivarse a sí mismo
            form.cleaned_data['is_active'] = True
            form.save()
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('perfil_usuario')
        else:
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'usuarios/perfil_usuario.html', {
        'form': form,
        'usuario': request.user
    })

@login_required
def listar_usuarios(request):
    """Vista para listar todos los usuarios"""
    usuarios = CustomUser.objects.all().order_by('username')
    return render(request, 'usuarios/listar_usuarios.html', {
        'usuarios': usuarios,
        'total_usuarios': usuarios.count()
    })

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('iniciar_sesion')