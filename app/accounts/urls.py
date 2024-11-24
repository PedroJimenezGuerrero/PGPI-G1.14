from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/singin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('register/signup/', views.signup, name = 'signup'),
    path('profile/', view=views.profile, name= 'profile'),
    path('profile/logout/', view = views.logout_view, name = 'logout'),
    path('unregistered', view= views.unregistered, name = 'unregistered'),
    path('edit_profile/', view= views.edit_profile, name='edit_profile')
]