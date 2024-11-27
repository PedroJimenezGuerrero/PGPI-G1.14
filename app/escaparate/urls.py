from django.urls import path
from . import views

app_name = 'escaparate'

urlpatterns = [
    path('', views.escaparate, name='escaparate'),
    
]