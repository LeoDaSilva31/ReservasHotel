# aplicaciones/reservations/urls.py
from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.ReservationListView.as_view(), name='list'),
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='detail'),
    path('create/', views.ReservationCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ReservationUpdateView.as_view(), name='update'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/events/', views.CalendarView.as_view(), name='calendar_events'),
]