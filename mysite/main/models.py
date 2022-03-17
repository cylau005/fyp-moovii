from django.db import models
from django.contrib.auth.models import User
from django.forms import IntegerField
#from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager

# Create your models here.
# class ToDoList(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class Item(models.Model):
#     todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
#     text = models.CharField(max_length=300)
#     complete = models.BooleanField()

#     def __str__(self):
# #        return self.text

class MovieList(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_name =  models.CharField(max_length=100, blank=True)
    movie_genre = models.CharField(max_length=100, blank=True)
    overall_rating = models.IntegerField(default=None, blank=True, null=True)
    date_release = models.DateField(default=None, blank=True, null=True)
    movie_image_url = models.CharField(max_length=255, default=None, blank=True, null=True)


class RatingList(models.Model):
    id = models.AutoField(primary_key=True)
    #user_id = models.IntegerField(default=None, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_rating = models.DateField(default=None, blank=True, null=True)
    rating_score = models.IntegerField(default=None, blank=True, null=True)
    movie_id = models.IntegerField(default=None, blank=True, null=True)
    action = models.CharField(
        max_length=20,
        choices=[('Rate','Rate'),
                ('Share','Share'),],
        default=None, blank=True, null=True)
    
  
class PrizeList(models.Model):
    item_id = models.IntegerField(primary_key=True)
    item_name =  models.CharField(max_length=100)
    require_points = models.IntegerField()


class Reward_Point(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=None, blank=True, null=True)
    date_modified = models.DateField(default=None, blank=True, null=True)
    redeem_item_id = models.ForeignKey(PrizeList, on_delete=models.CASCADE, default=None, blank=True, null=True)