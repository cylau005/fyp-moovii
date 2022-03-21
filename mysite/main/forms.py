from django import forms
from django.contrib.auth.models import User
from .models import RatingList, Reward_Point, MovieList

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

RATE_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]

ACTION_CHOICES = [
    ('Rate','Rate'),
    ('Share','Share'),
]

PRIZE_CHOICES = [
    (1,"Movie Ticket"),
    (2,"Cinema Food Voucher"),
    (3,"One Month Subscription"),
]

class RatingForm(forms.Form):
    rating_score = forms.IntegerField(label='Rating Score', 
                  widget=forms.Select(choices=RATE_CHOICES))
    movie_id = forms.IntegerField(label='Movie ID')
    action = forms.CharField(label='Rate or Share', 
            widget=forms.Select(choices=ACTION_CHOICES))

    class Meta:
        model = RatingList
        fields = ["rating_score", "movie_id", "action"]
  
class RedeemForm(forms.Form):
    redeem_item_id = forms.IntegerField(label='Prize ID', 
                  widget=forms.Select(choices=PRIZE_CHOICES))
    
    class Meta:
        model = Reward_Point
        fields = ["redeem_item_id"]

class AddMovieForm(forms.Form):
    id = forms.IntegerField(label='Movie ID')
    movie_name = forms.CharField(label='Movie Name')
    movie_genre = forms.CharField(label='Movie Genre')
    overall_rating = forms.CharField(label='Overall Rating')
    date_release = forms.DateField(label='Date Released')
    movie_image_url = forms.CharField(label='Movie Image URL')

    class Meta:
        model = MovieList
        fields = ["id","movie_name","movie_genre","overall_rating","date_release","movie_image_url"]

class AddRatingForm(forms.Form):
    user_id = forms.CharField(label='User ID')
    movie_id = forms.CharField(label='Movie ID')
    rating_score = forms.CharField(label='Rating Score')
    action = forms.CharField(label='Rate or Share', 
            widget=forms.Select(choices=ACTION_CHOICES))
    
    class Meta:
        model = RatingList
        fields = ["user_id","movie_id","rating_score","action"]