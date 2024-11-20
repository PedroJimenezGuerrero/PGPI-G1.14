from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login

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
    usernameOrEmail = request.POST['username']     #Si se inicia sesión con email, 'username' será un correo
    password = request.POST['password']
    
    user = authenticate(request, username=usernameOrEmail, password=password)
    if user is None:
        username = User.objects.get(email__exact = usernameOrEmail).get_username()
        user = authenticate(request, username=username, password=password)         # Si falla autenticación con correo lo intenta con nombre de usuario
    if user is not None:
        login(request, user, user.backend)
        return redirect('/')
    else:
        print('Account does not exist, returning HTTP response')
        return render(request, 'login/login.html', {'errorclass':'alert alert-danger','error': 'Sorry. No such account exists. Consider signing up!'})
    


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
    print(emailExists)
    print(nameExists)   
    # if nameExists is None and emailExists is None:
    #     if password == password1:
    #         User.objects.create_user(username=username, email=email, password=password)
    #         print('Registered new user, returning HTTP response')
    #         user = authenticate(request, username = username, email=email, password=password)
    #         login(request, user, user.backend)
    #         return redirect('/accounts/profile')
    #     else:
    #         print('Passwords do not match, returning HTTP response')
    #         return render(request, 'register/register.html', {'errorclass':'alert alert-danger','error': 'Sorry. The Passwords do not match.'})
    # else:
    #     print('The Username or Email ID is already taken, returning HTTP response')
    #     return render(request, 'register/register.html', {'errorclass':'alert alert-danger','error': 'Sorry. The Username or Email ID is already taken.'})
    
    if nameExists and emailExists:
        print('The Username or Email ID is already taken, returning HTTP response')
        return render(request, 'register/register.html', {'errorclass':'alert alert-danger','error': 'Sorry. The Username or Email ID is already taken.'})
    else:
        if password == password1:
            User.objects.create_user(username=username, email=email, password=password)
            print('Registered new user, returning HTTP response')
            user = authenticate(request, username = username, email=email, password=password)
            login(request, user, user.backend)
            return redirect('/accounts/profile')
        else:
            print('Passwords do not match, returning HTTP response')
            return render(request, 'register/register.html', {'errorclass':'alert alert-danger','error': 'Sorry. The Passwords do not match.'})
        
    
    
def profile(request):
    return render(request,'user/profile.html') 

def logout_view(request):
    logout(request)
    return redirect('/')

def unregistered(request):
    return render(request, 'user/unregistered.html')