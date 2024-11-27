from django import forms
from .models import Room, RoomType

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'room_type', 'floor', 'is_active', 'notes']