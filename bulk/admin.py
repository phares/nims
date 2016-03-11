from django.contrib import admin
from.models import User,Transactions, Wallet

# Register your models here.

class UserModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "first_name","last_name","email","organization","register_date_time"]
    list_display_links = ["organization"]
    list_filter = ["first_name"]
    search_fields = ["email","organization"]
    class Meta:
        model = User

class TransactionsModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "first_name","last_name","mobile_number","transaction_amount","transaction_code", "organization", "user_key"]
    list_display_links = ["transaction_amount"]
    list_filter = ["organization"]
    search_fields = ["mobile_number","transaction_code"]
    class Meta:
        model = Transactions

class WalletModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "balance","organization","status","user_key","last_transaction_date"]
    list_display_links = ["organization"]
    list_filter = ["status"]
    search_fields = ["user_key","organization"]
    class Meta:
        model = Wallet

admin.site.register(User, UserModelAdmin)
admin.site.register(Transactions, TransactionsModelAdmin)
admin.site.register(Wallet, WalletModelAdmin)


