from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import Reservation
from aplicaciones.rooms.models import Room
from .forms import ReservationForm, ReservationStatusForm

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Q
from datetime import date, datetime

from datetime import datetime, time, timedelta
from django.utils import timezone


# Vista para listar todas las reservas
class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'
    
    # Aquí podrías agregar el filtro por estado
    def get_queryset(self):
        queryset = Reservation.objects.all().select_related('room', 'created_by')
        status = self.request.GET.get('status')
    
        checkout_time = time(10, 0)  # 10:00 AM
        for reservation in queryset:
            checkout_datetime = datetime.combine(
                reservation.check_out, 
                checkout_time
            ).replace(tzinfo=timezone.get_current_timezone())
            alert_start = checkout_datetime - timedelta(days=1)
            
            reservation.show_alert = (
                timezone.now() >= alert_start and 
                timezone.now() <= checkout_datetime and
                reservation.status not in ['checked_out', 'cancelled']
            )
        
        if status:
                queryset = queryset.filter(status=status)
        return queryset

    # Agregar este método para enviar los estados al template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Usar las tuplas completas de STATUS_CHOICES para tener valor y display
        context['estados'] = Reservation.STATUS_CHOICES
        context['selected_status'] = self.request.GET.get('status', '')
        return context

class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_form'] = ReservationStatusForm(instance=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReservationStatusForm(request.POST, instance=self.object)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado de reserva actualizado correctamente.')
            return redirect('reservations:detail', pk=self.object.pk)
        
        context = self.get_context_data(object=self.object)
        context['status_form'] = form
        return self.render_to_response(context)

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Reservation
from .forms import ReservationForm

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservations:list')

    def get_initial(self):
        initial = super().get_initial()
        initial['check_in'] = date.today()
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservations:list')

# Vista del calendario
class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'reservations/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene todas las habitaciones
        context['rooms'] = Room.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        # Si la URL contiene 'events', devuelve los eventos del calendario
        if 'events' in request.path:
            return self.get_events(request)
        return super().get(request, *args, **kwargs)

    def get_events(self, request):
        """Obtiene los eventos para el calendario"""
        # AQUÍ ES DONDE PUEDES MODIFICAR QUÉ ESTADOS SE MUESTRAN
        # Cambia esta línea para excluir más estados:
        reservations = Reservation.objects.select_related('room').exclude(
            status__in=['cancelled', 'checked_out']  # Agrega más estados aquí
        )

        # O alternativamente, filtra solo por los estados que quieres mostrar:
        # reservations = Reservation.objects.select_related('room').filter(
        #     status__in=['confirmed', 'pending', 'pre_reserved', 'checked_in']
        # )

        events = []
        # Define los colores para cada estado
        for reservation in reservations:
            color = {
                'confirmed': '#28a745',    # verde
                'pending': '#ffc107',      # amarillo
                'pre_reserved': '#17a2b8', # azul
                'checked_in': '#6f42c1',   # morado
                'checked_out': '#6c757d',  # gris
            }.get(reservation.status, '#dc3545')  # rojo por defecto

            events.append({
                'id': reservation.id,
                'title': f'{reservation.room.number} - {reservation.guest_name}',
                'start': reservation.check_in.isoformat(),
                'end': reservation.check_out.isoformat(),
                'color': color,
                'url': reverse('reservations:detail', args=[reservation.id]),
                'resourceId': reservation.room.id,
            })

        return JsonResponse(events, safe=False)
    
def get_events(self, request):
    """API endpoint para obtener eventos del calendario"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    print(f"Solicitando eventos desde {start} hasta {end}")  # Debug
    
    reservations = Reservation.objects.select_related('room').exclude(
        status='cancelled'
    )
    
    if start and end:
        reservations = reservations.filter(
            check_out__gte=start,
            check_in__lte=end
        )
    
    events = []
    for reservation in reservations:
        events.append({
            'id': reservation.id,
            'title': f'{reservation.room.number} - {reservation.guest_name}',
            'start': reservation.check_in.isoformat(),
            'end': reservation.check_out.isoformat(),
            'color': {
                'confirmed': '#28a745',
                'pending': '#ffc107',
                'pre_reserved': '#17a2b8',
                'checked_in': '#6f42c1',
                'checked_out': '#6c757d',
            }.get(reservation.status, '#dc3545'),
            'url': reverse('reservations:detail', args=[reservation.id]),
            'resourceId': reservation.room.id,
        })
    
    print(f"Enviando {len(events)} eventos")  # Debug
    return JsonResponse(events, safe=False)