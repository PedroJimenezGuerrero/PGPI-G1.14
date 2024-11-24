from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
import re

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
        
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Excluir campos no deseados explícitamente
        if 'password' in self.fields:
            del self.fields['password']
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return password