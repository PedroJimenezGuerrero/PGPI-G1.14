from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['email'].initial = user.email

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'address': 'Dirección',
            'postal_code': 'Código Postal',
            'city': 'Ciudad'
        }
