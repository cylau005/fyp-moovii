from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import MovieList, RatingList, Reward_Point
from .resources import MovieListResources, RatingListResources, RewardPointResources
from django.contrib import messages
from tablib import Dataset
from django.db.models import Sum
from django.views.generic.list import ListView
from .forms import RatingForm

# Create your views here.
def home(response):
    return render(response, "main/home.html", {})

def view(response):
    return render(response, "main/view.html", {})

def profile(response):
    data = RatingList.objects.all().aggregate(thedata=Sum('rating_score'))
    #data = RatingList.objects.values('user_id').annotate(thedata=Sum('rating_score'))
    return render(response, "main/profile.html", {"data":data})
    #return render(response, "main/profile.html", {})

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

