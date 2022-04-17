from django import forms
from django.contrib.auth.models import User
from .models import RatingList, Reward_Point, MovieList, PrizeList

# Fixed rating score from 1 to 5
RATE_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]

# Fixed action for rating and sharing
ACTION_CHOICES = [
    ('Rate','Rate'),
    ('Share','Share'),
]

# Form for rating
class RatingForm(forms.Form):
    rating_score = forms.IntegerField(label='Rating Score', 
        widget=forms.Select(choices=RATE_CHOICES))
    movie_id = forms.IntegerField(label='Movie ID')
    action = forms.CharField(label='Rate or Share', 
        widget=forms.Select(choices=ACTION_CHOICES))

    class Meta:
        model = RatingList
        fields = ["rating_score", "movie_id", "action"]

# Form for adding movie
class AddMovieForm(forms.Form):
    movie_name = forms.CharField(label='Movie Name')
    movie_genre = forms.CharField(label='Movie Genre')
    overall_rating = forms.CharField(label='Overall Rating')
    date_release = forms.DateField(label='Date Released')
    movie_image_url = forms.CharField(label='Movie Image URL')

    class Meta:
        model = MovieList
        fields = ["movie_name","movie_genre","overall_rating","date_release","movie_image_url"]

# Form for adding rating
class AddRatingForm(forms.Form):
    user_id = forms.CharField(label='User ID')
    movie_id = forms.CharField(label='Movie ID')
    rating_score = forms.IntegerField(label='Rating Score', 
                  widget=forms.Select(choices=RATE_CHOICES))
    
    class Meta:
        model = RatingList
        fields = ["user_id","movie_id","rating_score"]

# Form for deleting rating
class DeleteRatingForm(forms.Form):
    id = forms.IntegerField(label='Rating ID')

    class Meta:
        model = RatingList
        fields = ["id"]

# Form for searching movie
class MovieSearchForm(forms.Form):
    movie_name = forms.CharField(label='movie_name')

    class Meta:
        model = MovieList
        fields = ["movie_name"]

# Form for searching user
class UserSearchForm(forms.Form):
    username = forms.CharField(label='username')

    class Meta:
        model = User
        fields = ["username"]

# Form for deleteing movie
class DeleteMovieForm(forms.Form):
    movie_name = forms.CharField(label='Movie Name')

    class Meta:
        model = MovieList
        fields = ["movie_name"]