from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import MovieList, RatingList, Reward_Point, PrizeList
from .resources import MovieListResources, RatingListResources, RewardPointResources
from django.contrib import messages
from tablib import Dataset
from django.db.models import Sum
from django.views.generic.list import ListView
from .forms import RatingForm, RedeemForm, AddMovieForm, AddRatingForm
import string    
import random 

# Create your views here.
def home(response):
    return render(response, "main/home.html", {})

def view(response):
    return render(response, "main/view.html", {})

def profile(response):
    user = response.user
    data = Reward_Point.objects.filter(user_id=user).aggregate(thedata=Sum('point'))
    prize = PrizeList.objects.all()
    reward = Reward_Point.objects.filter(user_id=user).order_by('date_modified')

    if response.method == "POST":
        form = RedeemForm(response.POST)
        if form.is_valid():
            
            point = data['thedata']
            
            if point >= 1:    
                item = form.cleaned_data["redeem_item_id"]
                point = 0-1
                S = 30
                ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
                
                if item == 1:
                    ran = 'MV-'+ran
                    msg = 'Please do a screenshot and present it to the staff  \n\n' + ran

                if item == 2:
                    ran = 'FD-'+ran
                    msg = 'Please do a screenshot and present it to the staff  \n\n' + ran

                if item == 3:
                    ran = 'One month subscription'
                    msg = 'We will extend your subscription for one month'
                
                r = Reward_Point(user_id=user, point=point, redeem_item_id=item, code = ran)
                r.save()
            
            else:
                msg = 'You do not have enough point'

        
        return render(response, "main/profile.html", {"data":data, "prize":prize, "form":form, "msg":msg, "reward":reward})
        
    else:
        form = RedeemForm()
        rating_form = Reward_Point()

    return render(response, "main/profile.html", {"data":data, "prize":prize, "form":form, "reward":reward})

def aboutus(response):
    return render(response, "main/aboutus.html", {})

def movie_upload(request):
    if request.method == 'POST':
        movie_resource = MovieListResources()
        dataset = Dataset()
        new_movie = request.FILES['myfile']

        if not new_movie.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'upload.html')

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
    return render(request, 'upload.html')

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


def movieListing(request):
    movies = MovieList.objects.all()
    return render(request, "main/movie_listing.html", {"movielist": movies})


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
            t = MovieList(id=i, movie_name=n, movie_genre=g, overall_rating=a, date_release=d, movie_image_url=u)
            msg = "Movie added"
            t.save()
        
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/movie_listing_add.html", {"msg":msg})
        
    else:
        form = AddMovieForm()
        add_movie_form = MovieList()
    
    return render(request, "main/movie_listing_add.html", {"form":form})


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
            u = request.user
            
            user = request.user
            print(user)

            if a == "Rate":
                p = 2
            else:
                p = 3
                s = None

            t = RatingList(user_id=u, rating_score=s, movie_id=m, action=a)
            r = Reward_Point(user_id=user, point=p)
            t.save()
            r.save()

            msg = "Rating added"
            print(msg)
            t.save()
        
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/rate_listing_add.html", {"msg":msg})
        
    else:
        form = AddRatingForm()
        add_movie_form = RatingList()
    
    return render(request, "main/rate_listing_add.html", {"form":form})
