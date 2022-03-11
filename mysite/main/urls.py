from django.urls import path
from . import views


urlpatterns = [
# path("<int:id>", views.index, name = "index"),
path("", views.home, name="home"),
path("home/", views.home, name="home"),
#path("create/", views.create, name="create"),
path("view/", views.view, name="view"),
path("profile/", views.profile, name="profile"),
path('movie_upload/', views.movie_upload, name="movie_upload"),
path('rating_upload/', views.rating_upload, name="rating_upload")
]