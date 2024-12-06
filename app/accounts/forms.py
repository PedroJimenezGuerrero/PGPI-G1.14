from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import Cliente 
import re

class EditProfileForm(UserChangeForm):
    direccion = forms.CharField(max_length=255, label='Dirección')
    metodo_pago = forms.ChoiceField(choices= Cliente.PAYMENT_METHOD_CHOICES, label='Método de Pago')
    codigo = forms.IntegerField(max_value=9999)
    ciudad = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'direccion', 'metodo_pago', 'codigo', 'ciudad']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'first_name' : 'Nombre',
            'last_name' : 'Apellidos',
            'direccion': 'Dirección de envío',
            'metodo_pago': 'Método de pago preferido', 
            'codigo': 'Código postal',
            'ciudad': 'Ciudad'
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
        if self.instance and hasattr(self.instance, 'cliente'):
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['direccion'].initial = self.instance.cliente.dirección
            self.fields['metodo_pago'].initial = self.instance.cliente.método_pago
            self.fields['codigo'].initial = self.instance.cliente.código_postal
            self.fields['ciudad'].initial = self.instance.cliente.ciudad

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        if commit:
            user.save()
            if hasattr(user, 'cliente'):
                cliente = user.cliente
            else:
                cliente = Cliente(user=user)
            cliente.dirección = self.cleaned_data['direccion']
            cliente.método_pago = self.cleaned_data['metodo_pago']
            cliente.código_postal = self.cleaned_data['codigo']
            cliente.ciudad = self.cleaned_data['ciudad']
            cliente.save()
        return user

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # direccion = forms.CharField(max_length=255, label='Dirección de envío')
    # metodo_pago = forms.ChoiceField(choices=Cliente.MetodosDePago.choices, label='Método de pago preferido')

    class Meta:
        model = User
        # fields = ['username', 'email', 'password1', 'password2', 'direccion', 'metodo_pago']
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return password

    # def save(self, commit=True):
    #     user = super(CustomUserCreationForm, self).save(commit=False)
    #     if commit:
    #         user.save()
    #         cliente = Cliente.objects.create(
    #             user=user,
    #             direccion=self.cleaned_data['direccion'],
    #             metodo_pago=self.cleaned_data['metodo_pago']
    #         )
    #     return user
