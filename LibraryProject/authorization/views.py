from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from .forms import LoginForm
# Create your views here.

def login_user(request):

    if request.user.is_authenticated:
        return redirect('/book-list')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/book-list')
            else:
                messages.error(request, "There was an error with your login.")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
    
def logout_user(request):
        logout(request)
        messages.success(request, ("LogIn to proceed"))
        return redirect('login')

def register_user(request):

    if request.user.is_authenticated:
        return redirect('/book-list')

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request=request, user=user)
            messages.success(request, "You logged in")
            return redirect('/book-list')
        else:
            messages.success(request, form.errors)
            return render(request, 'registration.html', {'form':form})
    else:
         form = RegisterUserForm()
         return render(request, 'registration.html', {'form':form})
    