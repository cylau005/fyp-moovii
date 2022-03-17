from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
path("", views.home, name="home"),
path("home/", views.home, name="home"),
path("profile/", views.profile, name="profile"),
path("movie_detail/", views.Rating, name="movie_detail"),

path('movie_upload/', views.movie_upload, name="movie_upload"),
path('rating_upload/', views.rating_upload, name="rating_upload"),

path('aboutus/', views.aboutus, name="aboutus"),

path('reset_password/', 
auth_views.PasswordResetView.as_view(template_name="main/password_reset.html"), name="reset_password"),
path('reset_password_sent/', 
auth_views.PasswordResetDoneView.as_view(template_name="main/password_reset_sent.html"), name="password_reset_done"),
path('reset/<uidb64>/<token>/', 
auth_views.PasswordResetConfirmView.as_view(template_name="main/password_reset_form.html"), name="password_reset_confirm"),
path('reset_password_complete/', 
auth_views.PasswordResetCompleteView.as_view(template_name="main/password_reset_done.html"), name="password_reset_complete"),
]

