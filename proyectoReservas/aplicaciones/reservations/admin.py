from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'guest_name',
        'room',
        'check_in',
        'check_out',
        'colored_status',
        'pre_reserve_status'
    ]
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['guest_name', 'guest_email', 'room__number']
    date_hierarchy = 'check_in'
    
    fieldsets = (
        ('Información de la Reserva', {
            'fields': (
                'room', 
                ('check_in', 'check_out'), 
                'status',
                'pre_reserve_expires'
            ),
            'classes': ('wide',)
        }),
        ('Información del Huésped', {
            'fields': (
                'guest_name', 
                'guest_email', 
                'guest_phone'
            ),
            'classes': ('wide',)
        }),
        ('Información Adicional', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

    def colored_status(self, obj):
        """Mostrar estado con color"""
        return format_html(
            '<span class="status-{}">{}</span>',
            obj.status,
            obj.get_status_display()
        )
    colored_status.short_description = 'Estado'

    def pre_reserve_status(self, obj):
        """Muestra el estado de la pre-reserva y tiempo restante"""
        if obj.status == 'pre_reserved' and obj.pre_reserve_expires:
            if obj.pre_reserve_expires < timezone.now():
                return format_html(
                    '<span class="status-cancelled">❌ Expirada</span>'
                )
            time_left = obj.pre_reserve_expires - timezone.now()
            hours = int(time_left.total_seconds() / 3600)
            minutes = int((time_left.total_seconds() % 3600) / 60)
            return format_html(
                '<span class="status-pre_reserved">⏳ Expira en {}h {}m</span>',
                hours, minutes
            )
        return '-'
    pre_reserve_status.short_description = 'Estado Pre-reserva'

    def get_readonly_fields(self, request, obj=None):
        """Hace los campos de solo lectura si la pre-reserva está expirada"""
        if obj and obj.status == 'pre_reserved' and obj.pre_reserve_expires < timezone.now():
            return ['status', 'pre_reserve_expires'] + list(self.readonly_fields)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:  # Solo asignar si es nuevo
            obj.created_by = request.user
        try:
            obj.save()
        except ValidationError as e:
            form.add_error(None, e)
            raise

    def get_list_display_links(self, request, list_display):
        """Hacer que el nombre del huésped sea un enlace"""
        return ['guest_name']

    class Media:
        css = {
            'all': ('admin/css/reservation.css',)
        }
        js = ('admin/js/reservation.js',)