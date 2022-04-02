from django.contrib import admin
from .models import Account, CreditCard, BankIn
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import NotRegistered
# Register your models here.

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class AccountCredit(admin.StackedInline):
    model = CreditCard
    can_delete = False
    verbose_name_plural = 'Credit Card'

class CustomizedUserAdmin (UserAdmin):
    inlines = (AccountInline, AccountCredit, )


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

admin.site.register(Account)
admin.site.register(CreditCard)
admin.site.register(BankIn)