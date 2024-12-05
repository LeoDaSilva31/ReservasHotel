from django import forms
from .models import Reservation
from datetime import date

class ReservationForm(forms.ModelForm):
   class Meta:
       model = Reservation
       fields = ['room', 'guest_name', 'guest_email', 'guest_phone', 'check_in', 'check_out', 'status']
       widgets = {
           'room': forms.Select(attrs={'class': 'form-select'}),
           'guest_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del huésped'}),
           'guest_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email del huésped'}),
           'guest_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono del huésped'}),
           'check_in': forms.DateInput(
               attrs={
                   'class': 'form-control',
                   'type': 'date'
               },
               format='%Y-%m-%d'
           ),
           'check_out': forms.DateInput(
               attrs={
                   'class': 'form-control',
                   'type': 'date'
               },
               format='%Y-%m-%d'
           ),
           'status': forms.Select(attrs={'class': 'form-select'})
       }

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       instance = getattr(self, 'instance', None)
       
       if instance and instance.pk:
           self.fields['check_in'].widget.attrs['value'] = instance.check_in.strftime('%Y-%m-%d')
           self.fields['check_out'].widget.attrs['value'] = instance.check_out.strftime('%Y-%m-%d')
           self.fields['check_in'].widget.attrs['readonly'] = True
           self.fields['check_in'].widget.attrs['disabled'] = True
           self.fields['check_in'].required = False
       else:
           self.initial['check_in'] = date.today()

   def clean(self):
       cleaned_data = super().clean()
       check_in = cleaned_data.get('check_in')
       check_out = cleaned_data.get('check_out')
       instance = getattr(self, 'instance', None)

       if instance and instance.pk:
           check_in = instance.check_in
           cleaned_data['check_in'] = check_in

       if check_in and check_out and check_out <= check_in:
           raise forms.ValidationError('La fecha de salida debe ser posterior a la fecha de entrada.')

       return cleaned_data


class ReservationStatusForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }