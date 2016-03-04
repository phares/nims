from django.contrib import admin
from.models import User,Transactions, Wallet

# Register your models here.

admin.site.register(User)
admin.site.register(Transactions)
admin.site.register(Wallet)

