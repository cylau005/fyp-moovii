from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Account

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            
            
            g = form.cleaned_data["genres"]
            user = form.save()

            t = Account(user=user, genres=g)
            t.save()
        return redirect("/home")
    else:
        form = RegisterForm()
        account_form = Account()
    
    return render(request, "register/register.html", {"form":form})