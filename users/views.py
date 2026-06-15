from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from .models import StUser, Teacher
from .forms import SignUpForm, SignInForm

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect('users:signin')

    return wrapper

def teacher_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_teacher():
            return func(request, *args, **kwargs)

        return redirect('chat:room_list')  
    return wrapper

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = StUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data.get('email', ''),
                phone_number=form.cleaned_data.get('phone_number', ''),
                role=form.cleaned_data.get('role'),
                password=form.cleaned_data['password'],
            )
            if user.is_teacher():
                Teacher.objects.create(user=user)
                login(request, user)           
                return redirect('chat:create_room')  
            login(request, user) 
            return redirect('chat:room_list')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_teacher():
                    login(request, user)           
                    return redirect('chat:create_room')  
                login(request, user)
                return redirect('chat:room_list') #
            return render(request, 'signin.html', {
                'form': form,
                'error_message': 'Неверный логин или пароль'
            })
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('users:signin')