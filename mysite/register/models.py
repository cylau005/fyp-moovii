from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
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

class CreditCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cc_number = models.CharField(verbose_name="cc_number", max_length=16, unique=True)
    cc_name = models.CharField(verbose_name="cc_name", max_length=40, unique=True)
    cc_expirydate = models.CharField(verbose_name="cc_expirydate", max_length=10, unique=True)
    cc_cvv = models.CharField(verbose_name="cc_expirydate", max_length=3, unique=True)
    
    def __str__(self):
        return self.user.username
# class MyUserManager(BaseUserManager):
#     def create_user(self, username, email, first_name, 
#     last_name, cc_number, cc_name, cc_expirydate, cc_cvv, genres, password=None):
#         if not username:
#             raise ValueError('username is required')
#         if not email:
#             raise ValueError('email is required')
#         if not first_name:
#             raise ValueError('first_name is required')
#         if not last_name:
#             raise ValueError('last_name is required')
#         if not cc_number:
#             raise ValueError('cc_number is required')
#         if not cc_name:
#             raise ValueError('cc_name is required')
#         if not cc_expirydate:
#             raise ValueError('cc_expirydate is required')
#         if not cc_cvv:
#             raise ValueError('cc_cvv is required')
#         if not genres:
#             raise ValueError('genres is required')
        
#         user = self.model(
#             username = username,
#             email = self.normalize_email(email),
#             first_name = first_name,
#             last_name = last_name,
#             cc_number = cc_number,
#             cc_name = cc_name,
#             cc_expirydate = cc_expirydate,
#             cc_cvv = cc_cvv,
#             genres = genres
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, username, email, first_name, 
#     last_name, cc_number, cc_name, cc_expirydate, cc_cvv, genres, password=None):
#         user = self.create_user(
#             username = username,
#             password = password,
#             first_name = first_name,
#             last_name = last_name,
#             cc_number = cc_number,
#             cc_name = cc_name,
#             cc_expirydate = cc_expirydate,
#             cc_cvv = cc_cvv,
#             genres = genres
#         )
#         user.is_admin = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user



# class MyUser(AbstractBaseUser):
#     username = models.CharField(verbose_name="username", max_length=60, unique=True)
#     email = models.EmailField(verbose_name="email address", max_length=60, unique=True)
#     date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
#     first_name = models.CharField(verbose_name="firstname", max_length=60, unique=True)
#     last_name = models.CharField(verbose_name="lastname", max_length=60, unique=True)
#     cc_number = models.CharField(verbose_name="cc_number", max_length=60, unique=True)
#     cc_name = models.CharField(verbose_name="cc_name", max_length=60, unique=True)
#     cc_expirydate = models.CharField(verbose_name="cc_expirydate", max_length=60, unique=True)
#     cc_cvv = models.CharField(verbose_name="cc_cvv", max_length=60, unique=True)
#     genres = models.CharField(
#     max_length=30,
#     choices=[('Adventure','Adventure'),
#             ('Comedy','Comedy'),
#             ('Action','Action'),
#             ('Drama','Drama'),
#             ('Crime','Crime'),
#             ('Children','Children'),
#             ('Mystery','Mystery'),
#             ('Documentary','Documentary'),
#             ('Animation','Animation'),
#             ('Thriller','Thriller'),
#             ('Horror','Horror'),
#             ('Fantasy','Fantasy'),
#             ('Western','Western'),
#             ('Film-Noir','Film-Noir'),
#             ('Romance','Romance'),
#             ('War','War'),
#             ('Sci-Fi','Sci-Fi'),
#             ('Musical','Musical'),])
#     last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
    
#     USERNAME_FIELD="username"

#     REQUIRED_FIELDS=['username','email','first_name','last_name','cc_number','cc_name','cc_expirydate','cc_cvv','genres']

#     objects = MyUserManager()
#     def __str__(self):
#         return self.username

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True