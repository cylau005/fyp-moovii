from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genres = models.CharField(
        max_length=30,
        choices=[('Adventure','Adventure'),
                ('Comedy','Comedy'),
                ('Action','Action'),
                ('Drama','Drama'),
                ('Crime','Crime'),
                ('Children','Children'),
                ('Mystery','Mystery'),
                ('Documentary','Documentary'),
                ('Animation','Animation'),
                ('Thriller','Thriller'),
                ('Horror','Horror'),
                ('Fantasy','Fantasy'),
                ('Western','Western'),
                ('Film-Noir','Film-Noir'),
                ('Romance','Romance'),
                ('War','War'),
                ('Sci-Fi','Sci-Fi'),
                ('Musical','Musical'),])
    
    def __str__(self):
        return self.user.username
