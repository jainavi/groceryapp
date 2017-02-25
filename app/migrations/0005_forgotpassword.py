# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-23 22:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_onlineorder_currency_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgotPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=40, unique=True)),
                ('email', models.EmailField(max_length=70)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_expired', models.BooleanField(default=0)),
            ],
        ),
    ]