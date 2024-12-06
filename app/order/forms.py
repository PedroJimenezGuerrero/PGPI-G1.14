from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            if hasattr(user, 'cliente'):
                self.fields['payment_method'].initial = user.cliente.método_pago
                self.fields['address'].initial = user.cliente.dirección
                self.fields['postal_code'].initial = user.cliente.código_postal
                self.fields['city'].initial = user.cliente.ciudad
        
        # self.fields['payment_method'].initial = 'tarjeta'  # Establecer el valor por defecto
        # if self.instance and hasattr(self.instance, 'cliente'):
        #     self.fields['address'].initial = self.instance.cliente.dirección
        #     self.fields['payment_method'].initial = self.instance.cliente.método_pago

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'payment_method', 'paid']
        widgets = {
            'paid': forms.HiddenInput(
                attrs={
                    'required': False
                })}
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'address': 'Dirección',
            'postal_code': 'Código Postal',
            'city': 'Ciudad',
            'payment_method': 'Método de Pago',
            'paid': 'Pagado'
        }
