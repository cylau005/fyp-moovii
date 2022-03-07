from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Account, CreditCard

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            
            g = form.cleaned_data["genres"]
            ccnumber = form.cleaned_data["cc_number"]
            ccname = form.cleaned_data["cc_name"]
            ccexpirydate = form.cleaned_data["cc_expirydate"]
            cccvv = form.cleaned_data["cc_cvv"]
            user = form.save()

            t = Account(user=user, genres=g)
            t.save()

            c = CreditCard(user=user, cc_number=ccnumber, cc_name=ccname, cc_expirydate=ccexpirydate, cc_cvv=cccvv)
            c.save()
        return redirect("/home")
    else:
        form = RegisterForm()
        account_form = Account()
        credit_form = CreditCard()
    
    return render(request, "register/register.html", {"form":form})