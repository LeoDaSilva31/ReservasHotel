from django import forms
from .models import Reservation
from datetime import date

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'guest_name', 'guest_email', 'guest_phone', 'check_in', 'check_out', 'status']
        widgets = {
            'room': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'guest_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nombre del huésped'}
            ),
            'guest_email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email del huésped'}
            ),
            'guest_phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Teléfono del huésped'}
            ),
            'check_in': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'value': date.today().strftime('%Y-%m-%d')
                }
            ),
            'check_out': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('check_in'):
            self.initial['check_in'] = date.today()
        
        # Añadir clases y placeholders
        self.fields['room'].label = 'Habitación'
        self.fields['guest_name'].label = 'Nombre del Huésped'
        self.fields['guest_email'].label = 'Email'
        self.fields['guest_phone'].label = 'Teléfono'
        self.fields['check_in'].label = 'Fecha de Entrada'
        self.fields['check_out'].label = 'Fecha de Salida'
        self.fields['status'].label = 'Estado'

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in > check_out:
                raise forms.ValidationError(
                    'La fecha de salida debe ser posterior a la fecha de entrada.'
                )
            if check_in < date.today():
                raise forms.ValidationError(
                    'La fecha de entrada no puede ser anterior a hoy.'
                )

        return cleaned_data


class ReservationStatusForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }