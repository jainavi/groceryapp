# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-12 20:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
