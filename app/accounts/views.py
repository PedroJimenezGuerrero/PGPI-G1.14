from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import EditProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.core.exceptions import ObjectDoesNotExist

#user1, password: usuario1
#user2, password: usuario2
#admin1, password: administrador1
#user3, password: user3
#user4, password user4

times = 0
def login_view(request):
    global times
    print('Login Page Opened!')
    # times += 1
    if request.user.is_authenticated:
        # User is logged in, perform actions accordingly
        return redirect('profile')
    else:
        # User is not logged in, redirect to login page
        return render(request, 'login/login.html', {})
    

def signin(request):
    print('Login Request Made!')
    username_or_email = request.POST.get('username')  # Nombre de usuario o correo
    password = request.POST.get('password')

    # Intenta autenticar directamente con el valor proporcionado
    user = authenticate(request, username=username_or_email, password=password)

    if user is None:  # Si no existe, intenta buscar con el correo
        try:
            username = User.objects.get(email=username_or_email).username  # Obtén el nombre de usuario real
            user = authenticate(request, username=username, password=password)
        except User.DoesNotExist:
            # Si no existe usuario con el correo proporcionado
            print('El usuario no existe.')
            return render(request, 'login/login.html', {
                'errorclass': 'alert alert-danger',
                'error': 'Esta cuenta no existe. Considere crear una.'
            })

    if user is not None:  # Si la autenticación es exitosa
        login(request, user)  # Inicia sesión
        return redirect('/')  # Redirige al inicio
    else:
        print('Credenciales incorrectas.')
        return render(request, 'login/login.html', {
            'errorclass': 'alert alert-danger',
            'error': 'Usuario o contraseña incorrectos. Intenta nuevamente.'
        })



def register(request):
    global times
    print('Register Page Opened!')
    times += 1
    current_url = request.path
    print(current_url)
    print(0)
    if request.path == '/register/signup/':
        report_loc = '../signup/'
    else: report_loc = 'signup/'
    return render(request, 'register/register.html', {'loc':report_loc,'error': ''})

def signup(request):
    print('Register Request Made!')
    print('Reading Data from JSON')
    email = request.POST['email']
    password = request.POST['password']
    password1 = request.POST['password1']
    username = request.POST['username']
    emailExists = User.objects.filter(email = email).exists()
    nameExists = User.objects.filter(username = username).exists()
    if nameExists and emailExists:
        print('The Username or Email ID is already taken, returning HTTP response')
        return render(request, 'register/register.html', {'errorclass':'alert alert-danger','error': 'El usuario o correo ya están en uso.'})
    else:
        if password == password1:
            User.objects.create_user(username=username, email=email, password=password)
            print('Registered new user, returning HTTP response')
            user = authenticate(request, username = username, email=email, password=password)
            login(request, user, user.backend)
            return redirect('/accounts/profile')
        else:
            print('Passwords do not match, returning HTTP response')
            return render(request, 'register/register.html', {'errorclass':'alert alert-danger','error': 'La contrseña no coincide.'})
        

def profile(request):
    return render(request,'user/profile.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def unregistered(request):
    return render(request, 'user/unregistered.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
        else:
            print(form.errors)  # Imprime los errores del formulario
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/accounts/profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register/register.html', {'form': form})