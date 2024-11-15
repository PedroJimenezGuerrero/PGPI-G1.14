from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view),
    path('login/singin/', views.signin),
    path('register/', views.register),
    path('register/signup/', views.signup),
    path('profile/', view=views.profile, name= 'profile'),
    path('profile/logout/', view = views.logout_view),
    path('unregistered', view= views.unregistered)
]