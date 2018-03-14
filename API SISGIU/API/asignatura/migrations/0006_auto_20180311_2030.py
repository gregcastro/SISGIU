# Generated by Django 2.0 on 2018-03-11 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asignatura', '0005_prelacionasignatura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prelacionasignatura',
            name='asignatura_objetivo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prelacionasignatura_asignatura_objetivo', to='asignatura.Asignatura', to_field='codigo'),
        ),
        migrations.AlterField(
            model_name='prelacionasignatura',
            name='asignatura_prela',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prelacionasignatura_asignatura_prela', to='asignatura.Asignatura', to_field='codigo'),
        ),
    ]