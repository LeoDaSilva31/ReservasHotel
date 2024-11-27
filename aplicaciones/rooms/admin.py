from django.contrib import admin
from .models import Room, RoomType

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity']
    search_fields = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'room_type', 'floor', 'is_active']
    list_filter = ['is_active', 'room_type', 'floor']
    search_fields = ['number']