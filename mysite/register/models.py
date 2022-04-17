from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

# Create your models here.

# Model to keep favourite genre and DOB
# Genre default as below choices list, but will be overwritten by the Genres from MovieList model
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(default=None, blank=True, null=True)
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


# Model to keep credit card subscription
class CreditCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cc_number = CardNumberField('card number')
    cc_name = models.CharField(verbose_name="cc_name", max_length=40)
    cc_expirydate = CardExpiryField('expiration date')
    cc_cvv = SecurityCodeField('security code')
    subscription_enddate = models.DateTimeField(default=timezone.now()+timedelta(days=30))

    def __str__(self):
        return self.user.username

# Model to keep bank in payment subscription
class BankIn(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_enddate = models.DateTimeField(default=timezone.now()+timedelta(days=30))

    def __str__(self):
        return self.user.username