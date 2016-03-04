from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    '''
    Define the nims users table
    '''
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    organization = models.CharField(max_length=50)
    register_date_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.organization

class Transaction(models.Model):
    '''
    Define nims transactions table
    '''
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=10)
    transaction_amount = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_code = models.CharField(max_length=10)
    transaction_date_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    organization = models.CharField(max_length=50)
    user_key = models.ForeignKey(User)

    def __str__(self):
        return self.transaction_code

class Wallet(models.Model):
    '''
    Define nims wallet table
    '''

    balance = models.DecimalField(max_digits=6, decimal_places=2)
    organization = models.CharField(max_length=30)
    status = models.CharField(max_length=10)
    user_key = models.ForeignKey(User)
    last_transaction_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.organization