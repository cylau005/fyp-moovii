from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Account, CreditCard
from main.models import MovieList
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    # Get individual genres from MovieList
    movie = MovieList.objects.values_list("movie_genre", flat=True).distinct()
    total_movie = len(movie)
    genre_list = ''
    for i in movie:
        genre_list = genre_list + '|' + i
    split_genre = genre_list.split('|')
    split_genre = list(dict.fromkeys(split_genre))
    split_genre = list(filter(None, split_genre))
    msg = ''
    if request.method == "POST":
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]            
            g = request.POST['genres_chosen']
            ccnumber = form.cleaned_data["cc_number"]
            ccname = form.cleaned_data["cc_name"]
            ccexpirydate = form.cleaned_data["cc_expirydate"]
            cccvv = form.cleaned_data["cc_cvv"]
            
            
            # Unique username check
            user_check = User.objects.filter(username=username)
            email_check = User.objects.filter(email=email)
            ccnum_check = CreditCard.objects.filter(cc_number=ccnumber)
            print(email_check)
            print(user_check)
            print(ccnum_check)
            if not user_check and not email_check and not ccnum_check:
                msg = 'Account created'
                user = form.save()
                t = Account(user=user, genres=g)
                t.save()
                c = CreditCard(user=user, cc_number=ccnumber, cc_name=ccname, cc_expirydate=ccexpirydate, cc_cvv=cccvv)
                
                c.save()
                print('creditcard save')

            else:
                if user_check and email_check:
                    msg = 'Username/Email Address exist. Please try with others'
                else:
                    msg = 'Credit Card used in other account. Please try with other credit card'
                
                print(msg)
        
        else:
            msg = 'Username/Email Address exist. Please try with others'
            
        return render(request, "register/register.html", {"form":form, "split_genre":split_genre, "msg":msg})
    else:
        form = RegisterForm()
        account_form = Account()
        credit_form = CreditCard()
    
    return render(request, "register/register.html", {"form":form, "split_genre":split_genre, "msg":msg})