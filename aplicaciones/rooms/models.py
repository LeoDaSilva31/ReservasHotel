from django.db import models
from django.urls import reverse

class RoomType(models.Model):
    name = models.CharField('Tipo de Habitación', max_length=50)
    description = models.TextField('Descripción')
    capacity = models.IntegerField('Capacidad')
    
    class Meta:
        verbose_name = 'Tipo de Habitación'
        verbose_name_plural = 'Tipos de Habitaciones'
        ordering = ['name']

    def __str__(self):
        return self.name

class Room(models.Model):
    number = models.IntegerField(verbose_name='Número')
    room_type = models.ForeignKey(
        RoomType, 
        on_delete=models.PROTECT,
        verbose_name='Tipo de Habitación'
    )
    floor = models.IntegerField('Piso')
    is_active = models.BooleanField('Activa', default=True)
    notes = models.TextField('Notas', blank=True, null=True)
    created_at = models.DateTimeField('Creada', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizada', auto_now=True)
    
    class Meta:
        ordering = ['number']
        verbose_name = 'Habitación'
        verbose_name_plural = 'Habitaciones'

    def __str__(self):
        return f"Habitación {self.number} - {self.room_type}"

    def get_absolute_url(self):
        return reverse('rooms:room-detail', kwargs={'pk': self.pk})