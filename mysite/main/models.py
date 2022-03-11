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
#         return self.text

class MovieList(models.Model):
    id = models.IntegerField(primary_key=True)
    movie_name =  models.CharField(max_length=100)
    movie_name = models.CharField(max_length=100)
    overall_rating = models.IntegerField()
    date_release = models.DateField()
    movie_image_url = models.CharField(max_length=255)
