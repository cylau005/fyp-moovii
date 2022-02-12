from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.shortcuts import render
from django.contrib.auth import login, authenticate

# Create your views here.
# def register(response):
#     if response.method == "POST":
#         form = RegisterForm(response.POST)
#         if form.is_valid():
#             form.save()
        
#         return redirect("/home")
#     else:
#         form = RegisterForm()
    
#     return render(response, "register/register.html", {"form":form})

def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/home')
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})