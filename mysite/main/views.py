from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import MovieList, RatingList
from .resources import MovieListResources, RatingListResources, PrizeListResources
from django.contrib import messages
from tablib import Dataset
from django.db.models import Sum
from django.views.generic.list import ListView

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