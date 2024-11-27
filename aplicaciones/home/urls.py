   # aplicaciones/home/urls.py
from django.urls import path
from .views import bienvenida

urlpatterns = [
       path('', bienvenida, name='bienvenida'),
   ]