from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsTestCase(TestCase):
    def setUp(self):
        # Crear usuarios para las pruebas
        User.objects.create_user(username='user1', password='usuario1')
        User.objects.create_user(username='user2', password='usuario2')
        User.objects.create_user(username='admin1', password='administrador1')
        User.objects.create_user(username='user3', password='user3')
        User.objects.create_user(username='user4', password='user4')
        self.client = Client()

    def test_login_view(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_signin_view_valid_user(self):
        response = self.client.post(reverse('accounts:signup'), data= {'username': 'user1',
                                                                    'password': 'usuario1'})
        self.assertEqual(response.status_code, 302)  # Redirige después de iniciar sesión correctamente
        self.assertRedirects(response, '/')  # Verifica la redirección

    def test_signin_view_invalid_user(self):
        response = self.client.post(reverse('accounts:signup'), {'username': 'invalid',
                                                                 'password': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')

    def test_register_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/register.html')

    def test_signup_view(self):
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password',
            'password1': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Redirige después de registrarse correctamente
        self.assertRedirects(response, '/accounts/profile/')

    def test_signup_view_passwords_do_not_match(self):
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password',
            'password1': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/register.html')
        self.assertContains(response, 'The Passwords do not match')

    def test_profile_view(self):
        self.client.login(username='user1', password='usuario1')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    def test_logout_view(self):
        self.client.login(username='user1', password='usuario1')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # Redirige después de cerrar sesión
        self.assertRedirects(response, '/')

    def test_unregistered_view(self):
        response = self.client.get(reverse('accounts:unregistered'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/unregistered.html')
