from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import MovieList, RatingList, Reward_Point, PrizeList
from .resources import MovieListResources, RatingListResources, RewardPointResources
from django.contrib import messages
from tablib import Dataset
from django.db.models import Sum
from django.views.generic.list import ListView
from .forms import RatingForm, AddMovieForm, AddRatingForm, DeleteRatingForm, MovieSearchForm, UserSearchForm, DeleteMovieForm
import string    
import random 
from django.contrib.auth.models import User

# for CF related views
def movie_rating(request):  
    movies = MovieList.objects.all()
    ratings = RatingList.objects.all()
    return render(request, "main/movie_detail.html", {"movielist": movies})

def home(request):
    movies = MovieList.objects.all()

    if request.method == "POST":
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            movies_search = form.cleaned_data["movie_name"]
            movies_search_done = MovieList.objects.filter(movie_name__icontains=movies_search)
            
            if not movies_search_done:
                msg = 'No movie found'
                print(msg)
            else:
                movies = MovieList.objects.filter(movie_name__icontains=movies_search)
                msg = 'Please refer below'        
        return render(request, "main/home.html", {"movielist": movies,"form":form, "msg":msg})

    else:
        form = MovieSearchForm()
        movielist_form = MovieList()
    return render(request, "main/home.html", {"movielist": movies,"form":form})

def movies_detail_view(request, id):
    movie = MovieList.objects.get(id=id)
    genres = movie.movie_genre
    genresm = genres.replace('|',' | ')
    date = movie.date_release
    datem = date.year
    context= {'movie': movie,
              'movieyear':datem,
              'moviegenre':genresm,
              }
    
    return render(request, 'main/movie_detail.html', context)

def Rating(request):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["rating_score"]
            m = form.cleaned_data["movie_id"]
            a = form.cleaned_data["action"]
            user = request.user
            if a == "Rate":
                p = 2
            else:
                p = 3
                s = None

            t = RatingList(user_id=user, rating_score=s, movie_id=m, action=a)
            r = Reward_Point(user_id=user, point=p)
            t.save()
            r.save()

        return HttpResponseRedirect("/home")
        
    else:
        form = RatingForm()
        rating_form = RatingList()
    
    movies = MovieList.objects.all()
    return render(request, "main/movie_detail.html", {"form":form, "movielist": movies})

# default and profile views
def aboutus(response):
    return render(response, "main/aboutus.html", {})

def profile(response):
    user = response.user
    data = Reward_Point.objects.filter(user_id=user).aggregate(thedata=Sum('point'))
    prize = PrizeList.objects.all()
    reward = Reward_Point.objects.filter(user_id=user).order_by('date_modified')
    prizeItem = PrizeList.objects.all()

    if 'prize_chosen' in response.POST:
        
        item = response.POST['prize_chosen']
        point = data['thedata']
        
        if point >= 1:    
            point = 0-1
            S = 30
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
            
            if item == '1':
                ran = 'MV-'+ran
                msg = 'Please do a screenshot and present it to the staff  \n\n' + ran
                
            if item == '2':
                ran = 'FD-'+ran
                msg = 'Please do a screenshot and present it to the staff  \n\n' + ran
                
            if item == '3':
                ran = 'One month subscription'
                msg = 'We will extend your subscription for one month'
                
            r = Reward_Point(user_id=user, point=point, redeem_item_id=item, code = ran)
            r.save()
        
        else:
            msg = 'You do not have enough point'

        
        return render(response, "main/profile.html", {"data":data, "prize":prize, "prizeItem":prizeItem, "msg":msg, "reward":reward})
        
    else:
        error = "something wrong"

    return render(response, "main/profile.html", {"data":data, "prize":prize, "prizeItem":prizeItem, "reward":reward})

# admin views
def movie_upload(request):
    if request.method == 'POST':
        movie_resource = MovieListResources()
        dataset = Dataset()
        new_movie = request.FILES['myfile']

        if not new_movie.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'movie_upload.html')

        imported_data = dataset.load(new_movie.read(), format='xlsx')
        for data in imported_data:
            value = MovieList(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5]
            )
            value.save()
    return render(request, 'movie_upload.html')

def rating_upload(request):
    if request.method == 'POST':
        rating_resource = RatingListResources()
        dataset = Dataset()
        new_rating = request.FILES['myfile']

        if not new_rating.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'rating_upload.html')

        imported_data = dataset.load(new_rating.read(), format='xlsx')
        for data in imported_data:
            value = RatingList(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5]
            )
            value.save()
    return render(request, 'rating_upload.html')

def prize_upload(request):
    if request.method == 'POST':
        prize_resource = PrizeListResources()
        dataset = Dataset()
        new_prize = request.FILES['myfile']

        if not new_prize.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'prize_upload.html')

        imported_data = dataset.load(new_prizes.read(), format='xlsx')
        for data in imported_data:
            value = RatingList(
                data[0],
                data[1],
                data[2]
            )
            value.save()
    return render(request, 'prize_upload.html')

def reward_point_upload(request):
    if request.method == 'POST':
        reward_point_resource = RewardPointResources()
        dataset = Dataset()
        new_rp = request.FILES['myfile']

        if not new_rp.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'reward_point_upload.html')

        imported_data = dataset.load(new_rp.read(), format='xlsx')
        for data in imported_data:
            value = RatingList(
                data[0],
                data[1],
                data[2],
                data[3]
            )
            value.save()
    return render(request, 'reward_point_upload.html')

def movieListing(request): 
    movies = MovieList.objects.all()

    if request.method == "POST":
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            movies_search = form.cleaned_data["movie_name"]
            movies_search_done = MovieList.objects.filter(movie_name__icontains=movies_search)
            
            if not movies_search_done:
                msg = 'No movie found'
                print(msg)
            else:
                movies = MovieList.objects.filter(movie_name__icontains=movies_search)
                msg = 'Please refer below'
        
        return render(request, "main/movie_listing.html", {"movielist": movies,"form":form, "msg":msg})

    else:
        form = MovieSearchForm()
        movielist_form = MovieList()

        
    return render(request, "main/movie_listing.html", {"movielist": movies,"form":form})

def movieListingAdd(request):
    if request.method == "POST":
        form = AddMovieForm(request.POST)
        if form.is_valid():
            i = form.cleaned_data["id"]
            n = form.cleaned_data["movie_name"]
            g = form.cleaned_data["movie_genre"]
            a = form.cleaned_data["overall_rating"]
            d = form.cleaned_data["date_release"]
            u = form.cleaned_data["movie_image_url"]

            movie_check = MovieList.objects.filter(id=i)
            print(movie_check)
            if not movie_check:
                t = MovieList(id=i, movie_name=n, movie_genre=g, overall_rating=a, date_release=d, movie_image_url=u)
                msg = "Movie added"
                t.save()
            else:
                msg = "ID exists. Please try with other ID"
                
        
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/movie_listing_add.html", {"msg":msg})
        
    else:
        form = AddMovieForm()
        add_movie_form = MovieList()
    
    return render(request, "main/movie_listing_add.html", {"form":form})

def movieListingDelete(request):
    if request.method == "POST":
        form = DeleteMovieForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["id"]
            print(s)
            movie_check = MovieList.objects.filter(id=s)
            
            if not movie_check:
                msg = 'Movie not exists'
            else:
                MovieList.objects.filter(id=s).delete()
                msg = "Movie deleted"
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/movie_listing_delete.html", {"form":form,"msg":msg})
        
    else:
        form = DeleteMovieForm()
        delete_movie_form = MovieList()
    
    return render(request, "main/movie_listing_delete.html", {"form":form})

def rateListing(request):
    ratings = RatingList.objects.all()
    return render(request, "main/rate_listing.html", {"ratelist": ratings})

def rateListingAdd(request):
    if request.method == "POST":
        form = AddRatingForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["rating_score"]
            m = form.cleaned_data["movie_id"]
            a = form.cleaned_data["action"]
            u = form.cleaned_data["user_id"]
            user_check = User.objects.filter(username=u)
            print(user_check)

            if a == "Rate":
                p = 2
            else:
                p = 3
                s = None
            
            if not user_check:
                msg = 'User not exists'
                print(msg)

            else:
                user = User.objects.get(username=u)
                t = RatingList(user_id=user, rating_score=s, movie_id=m, action=a)
                r = Reward_Point(user_id=user, point=p)
                t.save()
                r.save()

                msg = "Rating added"
                print(msg)
            
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/rate_listing_add.html", {"form":form,"msg":msg})
        
    else:
        form = AddRatingForm()
        add_movie_form = RatingList()
    
    return render(request, "main/rate_listing_add.html", {"form":form})

def rateListingDelete(request):
    if request.method == "POST":
        form = DeleteRatingForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["id"]
            print(s)
            rating_check = RatingList.objects.filter(id=s)
            
            if not rating_check:
                msg = 'Rating not exists'

            else:
                RatingList.objects.filter(id=s).delete()
                msg = "Rating deleted"
            
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/rate_listing_delete.html", {"form":form,"msg":msg})
        
    else:
        form = DeleteRatingForm()
        delete_movie_form = RatingList()
    
    return render(request, "main/rate_listing_delete.html", {"form":form})

def userListing(request):
    users = User.objects.all()
    if request.method == "POST":
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            username_search_done = User.objects.filter(username__icontains=username)
            
            if not username_search_done:
                msg = 'No user found'
                print(msg)
            else:
                users = User.objects.filter(username__icontains=username)
                msg = 'Please refer below'
        
        return render(request, "main/user_listing.html", {"userlist": users,"form":form, "msg":msg})

    else:
        form = UserSearchForm()
        user_form = User()

    return render(request, "main/user_listing.html", {"userlist": users, "form":form})

def userBlacklist(request):
    if request.method == "POST":
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            username_search_done = User.objects.filter(username=username)
            
            if not username_search_done:
                msg = 'No user found'
                print(msg)
            else:
                users = User.objects.get(username=username)
                print(users)
                users.is_active = False
                users.save()
                msg = 'User blacklisted'
        
        return render(request, "main/user_blacklist.html", {"form":form, "msg":msg})

    else:
        form = UserSearchForm()
        user_form = User()

    return render(request, "main/user_blacklist.html", {"form":form})

