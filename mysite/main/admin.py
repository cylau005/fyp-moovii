from django.contrib import admin
from .models import ToDoList, Item#, MyUser, MyUserManager

# Register your models here.
admin.site.register(ToDoList)
admin.site.register(Item)
# admin.site.register(MyUser)
# admin.site.register(MyUserManager)