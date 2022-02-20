from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Account

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        account_form = Account(request.POST)

        if form.is_valid():
            g = form.cleaned_data["genres"]
            print(g)
            # t = Account(user=g)
            # t.save()
            user = form.save()
            account = account_form.save(commit=False)
            
            account.user = user
            account.genres = g

            account.save()
            

            form.save()
        
        return redirect("/home")
    else:
        form = RegisterForm()
        account_form = Account()
    
    return render(request, "register/register.html", {"form":form})