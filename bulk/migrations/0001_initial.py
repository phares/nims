# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-03 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=10)),
                ('mobile_number', models.CharField(max_length=10)),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('transaction_code', models.CharField(max_length=10)),
                ('transaction_date_time', models.DateTimeField(auto_now_add=True)),
                ('organization', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('organization', models.CharField(max_length=50)),
                ('register_date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=6)),
                ('organization', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=10)),
                ('last_transaction_date', models.DateTimeField(auto_now=True)),
                ('user_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulk.User')),
            ],
        ),
        migrations.AddField(
            model_name='transactions',
            name='user_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulk.User'),
        ),
    ]
