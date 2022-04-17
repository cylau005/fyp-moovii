from django.db import models
from django.contrib.auth.models import User
from django.forms import IntegerField


# Create your models here.

# Model to store all the movies
class MovieList(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_name =  models.CharField(max_length=100, blank=True)
    movie_genre = models.CharField(max_length=100, blank=True)
    overall_rating = models.IntegerField(default=None, blank=True, null=True)
    date_release = models.DateField(default=None, blank=True, null=True)
    movie_image_url = models.CharField(max_length=255, default=None, blank=True, null=True)

# Model to store all the rating and sharing
class RatingList(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField(default=None, blank=True, null=True)
    date_rating = models.DateField(auto_now_add=True)
    rating_score = models.IntegerField(default=None, blank=True, null=True)    
    action = models.CharField(
        max_length=20,
        choices=[('Rate','Rate'),
                ('Share','Share'),],
        default=None, blank=True, null=True)

# Model to store all the prize list
class PrizeList(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name =  models.CharField(max_length=100)
    require_points = models.IntegerField()

# Model to keep all reward point records
class Reward_Point(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=None, blank=True, null=True)
    date_modified = models.DateField(auto_now_add=True)
    redeem_item_id = models.ForeignKey(PrizeList, on_delete=models.CASCADE, default=None, blank=True, null=True)
    code = models.CharField(max_length=50,default=None, blank=True, null=True)

# Model to keep all the CF list for individual users
class CF_List(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    weighted_score = models.IntegerField(default=None, blank=True, null=True)
    movie_id = models.IntegerField(default=None, blank=True, null=True)
    movie_name = models.CharField(max_length=100, blank=True)
    movie_image_url = models.CharField(max_length=255, default=None, blank=True, null=True)