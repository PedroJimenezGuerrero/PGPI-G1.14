from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login

#user1, password: usuario1
#user2, password: usuario2
#admin1, password: administrador1

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
    # print('Reading Data from JSON')
    # json2 = open('user_data.json',) 
    # data = json.load(json2) 
    # l1 = data['u_data'][0]
    # emails = list(l1.keys())
    # passwords = list(l1.values())
    # json2.close() 
    # print('Read data from JSON')
    # global times
    # times = times+1
    # if request.path == '/login/signin/':
    #     report_loc = '../signin/'
    # else: report_loc = 'signin/'
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user, user.backend)
        return redirect('/')
    else:
        print('Account does not exist, returning HTTP response')
        return render(request, 'accounts/login.html', {'errorclass':'alert alert-danger','error': 'Sorry. No such account exists. Consider signing up!'})
    


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
    userExists = authenticate(request, username = username)
    if userExists is None:
        if password == password1:
            User.objects.create_user(username=username, email=email, password=password)
            print('Registered new user, returning HTTP response')
            user = authenticate(request, username = username, email=email, password=password)
            login(request, user, user.backend)
            return redirect('/accounts/profile')
        else:
            print('Passwords do not match, returning HTTP response')
            return render(request, 'register/register.html', {'errorclass':'alert alert-danger','error': 'Sorry. The Passwords do not match.'})
    else:
        print('The Username or Email ID is already taken, returning HTTP response')
        return render(request, 'register/register.html', {'errorclass':'alert alert-danger','error': 'Sorry. The Username or Email ID is already taken.'})
    
    
def profile(request):
    return render(request,'user/profile.html') 

def logout_view(request):
    logout(request)
    return redirect('/')

def unregistered(request):
    return render(request, 'user/unregistered.html')