# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='segundo_apellido',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='usuario',
            name='segundo_nombre',
            field=models.CharField(default='', max_length=50),
        ),
    ]
