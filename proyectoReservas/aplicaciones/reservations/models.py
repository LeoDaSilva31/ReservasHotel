from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import date, timedelta
from aplicaciones.rooms.models import Room

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pre_reserved', 'Pre-reservada'),
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('checked_in', 'Check-in'),
        ('checked_out', 'Check-out'),
        ('cancelled', 'Cancelada'),
    ]
    
    room = models.ForeignKey(
        Room, 
        on_delete=models.PROTECT,
        verbose_name='Habitación'
    )
    check_in = models.DateField(verbose_name='Fecha de entrada', default=date.today)
    check_out = models.DateField('Fecha de salida')
    guest_name = models.CharField('Nombre del huésped', max_length=100)
    guest_email = models.EmailField('Email del huésped')
    guest_phone = models.CharField('Teléfono del huésped', max_length=20)
    status = models.CharField(
        'Estado',
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Creado por'
    )
    created_at = models.DateTimeField('Creada', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizada', auto_now=True)
    notes = models.TextField('Notas', blank=True, null=True)
    # Campo para tiempo límite de pre-reserva
    pre_reserve_expires = models.DateTimeField(
        'Expiración de pre-reserva', 
        null=True, 
        blank=True
    )
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-check_in']

    def __str__(self):
        return f"Reserva {self.guest_name} - {self.check_in}"

    def get_absolute_url(self):
        return reverse('reservations:reservation-detail', kwargs={'pk': self.pk})
    
    def clean(self):
        """Validar que no haya reservas superpuestas para la misma habitación"""
        if self.check_in and self.check_out and self.room:
            # Verificar que check_out sea posterior a check_in
            if self.check_out <= self.check_in:
                raise ValidationError({
                    'check_out': _('La fecha de salida debe ser posterior a la fecha de entrada.')
                })

            # Buscar reservas superpuestas (excluyendo pre-reservas expiradas)
            overlapping = Reservation.objects.filter(
                room=self.room,
                check_in__lt=self.check_out,
                check_out__gt=self.check_in
            ).exclude(
                status='pre_reserved',
                pre_reserve_expires__lt=timezone.now()
            )

            # Excluir la reserva actual en caso de edición
            if self.pk:
                overlapping = overlapping.exclude(pk=self.pk)

            if overlapping.exists():
                raise ValidationError(
                    _('La habitación no está disponible en las fechas seleccionadas.')
                )

    def save(self, *args, **kwargs):
        # Si es pre-reserva y no tiene tiempo de expiración, establecer 24h
        if self.status == 'pre_reserved' and not self.pre_reserve_expires:
            self.pre_reserve_expires = timezone.now() + timedelta(hours=24)
        
        self.clean()
        super().save(*args, **kwargs)