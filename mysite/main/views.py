from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import MovieList, RatingList
from .resources import MovieListResources, RatingListResources
from django.contrib import messages
from tablib import Dataset

#from .models import ToDoList, Item
#from .forms import CreateNewList

# Create your views here.

# def index(response, id):
#     ls = ToDoList.objects.get(id=id)

#     if ls in response.user.todolist.all():

#         if response.method == "POST":
#             print(response.POST)
#             if response.POST.get("save"):
#                 for item in ls.item_set.all():
#                     if response.POST.get("c" + str(item.id)) == "clicked":
#                         item.complete = True
#                     else:
#                         item.complete = False
#                     item.save()

#             elif response.POST.get("newItem"):
#                 txt = response.POST.get("new")
#                 if len(txt)>2:
#                     ls.item_set.create(text=txt, complete=False)
#                 else:
#                     print("Invalid")

#         return render(response, "main/list.html", {"ls":ls})
#     return render(response, "main/view.html", {})



def home(response):
    return render(response, "main/home.html", {})

# def create(response):
#     if response.method == "POST":
#         form = CreateNewList(response.POST)
        
#         if form.is_valid():
#             n = form.cleaned_data["name"]
#             t = ToDoList(name=n)
#             t.save()
#             response.user.todolist.add(t)
        
#         return HttpResponseRedirect("/%i" %t.id)
#     else:
#         form = CreateNewList()
#     return render(response, "main/create.html", {"form":form})


def view(response):
    return render(response, "main/view.html", {})


def profile(response):
    return render(response, "main/profile.html", {})

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