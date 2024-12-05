# aplicaciones/usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Rol

class CustomUserCreationForm(UserCreationForm):
    # Campos de contraseña con widgets de tipo password
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Tu contraseña debe tener al menos 8 caracteres.'
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Ingresa la misma contraseña para verificación.'
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'nombre', 'apellido',
            'dni', 'telefono', 'rol'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.all()
        
        # Personalización de mensajes de error
        self.error_messages = {
            'password_mismatch': 'Las contraseñas no coinciden.',
            'username_exists': 'Este nombre de usuario ya está en uso.',
            'email_exists': 'Este correo electrónico ya está registrado.',
            'dni_exists': 'Este DNI ya está registrado.'
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['username_exists'])
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages['email_exists'])
        return email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if CustomUser.objects.filter(dni=dni).exists():
            raise forms.ValidationError(self.error_messages['dni_exists'])
        return dni

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nombre', 'apellido', 
                 'dni', 'telefono', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.all()
        
        # Hacer algunos campos opcionales en la edición
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
        self.fields['email'].help_text = 'Ingrese un correo electrónico válido.'
        self.fields['is_active'].help_text = 'Indica si el usuario debe ser tratado como activo. Desmarca esto en lugar de eliminar cuentas.'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Verificar si el username existe, excluyendo el usuario actual
        if CustomUser.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verificar si el email existe, excluyendo el usuario actual
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        # Verificar si el DNI existe, excluyendo el usuario actual
        if CustomUser.objects.filter(dni=dni).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Este DNI ya está registrado.')
        return dni
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nombre', 'apellido', 'dni', 'telefono']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }