from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
 class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

 
 """ first_name = forms.CharField(max_length=50)
 last_name = forms.CharField(max_length=50)
 email = forms.EmailField()
 address = forms.CharField(max_length=150)
 postal_code = forms.CharField(max_length=150)
 city = forms.CharField(max_length=100) """
    

