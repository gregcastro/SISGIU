# Generated by Django 2.0 on 2018-01-08 13:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0009_auto_20180107_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='fecha_nacimiento',
            field=models.DateField(default=datetime.date(2018, 1, 8)),
        ),
    ]
