from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/book-list')
        else:
            messages.success(request, ("There was an error"))
            return redirect('login')
    else:
        return  render(request, 'login.html')
    
def logout_user(request):
        logout(request)
        messages.success(request, ("LogIn to proceed"))
        return redirect('login')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data('username')
            password = form.cleaned_data('password1')
            user = authenticate(username, password)
            login(request=request, user=user)
            messages.success(request, "You logged in")
            return redirect('/book-list')
    else:
         form = UserCreationForm()
         return render(request, 'registration.html', {'form':form})