# aplicaciones/home/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def bienvenida(request):
    return render(request, 'home/bienvenida.html', {'rol': request.user.rol.nombre})