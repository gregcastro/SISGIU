# Generated by Django 2.0 on 2018-04-11 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
        ('periodo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='tipo_postgrado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuario.TipoPostgrado'),
        ),
    ]