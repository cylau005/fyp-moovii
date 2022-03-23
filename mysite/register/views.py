from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Account, CreditCard
from main.models import MovieList

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

    if request.method == "POST":
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            
            # g = form.cleaned_data["genres"]
            ccnumber = form.cleaned_data["cc_number"]
            ccname = form.cleaned_data["cc_name"]
            ccexpirydate = form.cleaned_data["cc_expirydate"]
            cccvv = form.cleaned_data["cc_cvv"]
            print(ccnumber)
            print(ccname)
            print(ccexpirydate)
            print(cccvv)
            g = request.POST['genres_chosen']
            print(g)

            user = form.save()


            t = Account(user=user, genres=g)
            t.save()

            c = CreditCard(user=user, cc_number=ccnumber, cc_name=ccname, cc_expirydate=ccexpirydate, cc_cvv=cccvv)
            c.save()
            print('creditcard save')
        return redirect("/register")
    else:
        form = RegisterForm()
        account_form = Account()
        credit_form = CreditCard()
    
    return render(request, "register/register.html", {"form":form, "split_genre":split_genre})