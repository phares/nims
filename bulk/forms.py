from django import forms
from .models import Transactions

class PostForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = [
            "first_name",
            "last_name",
            "mobile_number",
            "transaction_amount",
            "transaction_code",
            "organization",
            "user_key",
        ]
